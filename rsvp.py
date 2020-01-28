import logging

import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, \
    Filters, Updater, CallbackQueryHandler, ConversationHandler
import model

DBNAME = "evently"
import secrets

event_id = {"id": ""}
guest_info = {"brings": []}

COMING_OR_NOT, WHAT_TO_BRING, SUMMERY, FINISH = range(4)

logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater(token=secrets.BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

events_collection = model.get_collection(DBNAME, "events")


def cancel(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text="Goodbye")


def start(update: Update, context: CallbackContext):
    print(context.args)
    event_id['id'] = context.args[0]
    info_about_event = model.get_event(events_collection, event_id['id'])
    keyboard = [[InlineKeyboardButton("not this time", callback_data='0')],
                [InlineKeyboardButton("1", callback_data='1')],
                [InlineKeyboardButton("2", callback_data='2')],
                [InlineKeyboardButton("3", callback_data='3')],
                [InlineKeyboardButton("4", callback_data='4')],
                [InlineKeyboardButton("5", callback_data='5')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user_name = update.message.from_user.first_name
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    welcome_message = 'Hi, {} {} wants to know if you attend:{}'.format(user_name, info_about_event['name'],
                                                                        info_about_event['description'])
    update.message.reply_text(welcome_message, reply_markup=reply_markup)
    return COMING_OR_NOT


def coming_or_not(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    name = update.effective_user.first_name
    coll = model.get_collection(DBNAME, 'events')
    list_of_stuff = model.get_event(events_collection, event_id['id'])['items']  # get list of things left to brings
    guest_info['num_of_participants'] = update.callback_query.data  # how many people will arrive
    keyboard = [[InlineKeyboardButton("i don't want to bring anything, thanks", callback_data='no')]]
    model.rsvp(coll, event_id['id'], chat_id, name, guest_info['num_of_participants'])  # update the list of people
    goodbye_message = 'sorry to here your not coming {}, hope i see you soon'.format(name)
    coming_message = "see you soon {}, you will arrive as:{} people\n what would like to bring?".format(name,
                                                                                                        guest_info[
                                                                                                            'num_of_participants'])
    if guest_info['num_of_participants'] == '0':
        context.bot.send_message(chat_id=chat_id, text=goodbye_message)
    else:
        for item in list_of_stuff:
            keyboard.append([InlineKeyboardButton(item, callback_data=item)])
        context.bot.send_message(chat_id=chat_id, reply_markup=InlineKeyboardMarkup(keyboard), text=coming_message)
        print(list_of_stuff)
        return WHAT_TO_BRING


def what_to_bring(update: Update, context: CallbackContext):
    print(guest_info['brings'])
    user_id = update.effective_chat.id
    coll = model.get_collection(DBNAME, 'events')
    query = update.callback_query  # what he brings
    model.friend_brings_item(coll, event_id['id'], user_id, query.data)
    guest_info['brings'].append(query.data)
    list_of_stuff = model.get_event(events_collection, event_id['id'])['items']
    print(list_of_stuff)
    if guest_info['brings'] != 'no':
        keyboard = [[InlineKeyboardButton("no thanks, it enough", callback_data=' ')]]
        for item in list_of_stuff:
            keyboard.append([InlineKeyboardButton(item, callback_data=item)])
        next_message = 'you choose to brings {}, do you want to bring another things?'.format(query.data)
        context.bot.send_message(chat_id=user_id, reply_markup=InlineKeyboardMarkup(keyboard), text=next_message)
    return SUMMERY
    print(list_of_stuff)


def summery_message(update: Update, context: CallbackContext):
    name = update.effective_user.first_name
    chat_id = update.effective_chat.id
    coll = model.get_collection(DBNAME, 'events')
    query = update.callback_query
    if query.data != ' ':
        model.friend_brings_item(coll, event_id['id'], chat_id, query.data)
    guest_info['brings'].append(query.data)
    print(guest_info['brings'])
    print_items = '\n'
    participants_items = model.get_items(coll, event_id['id'])
    for participant in participants_items[0]:
        if participant['user_id'] == chat_id:
            for item in participant['brings']:
                print_items += item + '\n'

    final_message = 'thank for attending my event {},you arrive as:{} people\ndont forget to brings:{}\nsee you soon!!!'.format(
        name,
        guest_info['num_of_participants'], print_items)
    context.bot.send_message(chat_id=chat_id, text=final_message)
    return FINISH


def finish():
    pass


def respond(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text
    logger.info(f"= Got on chat #{chat_id}: {text!r}")
    response = update.message.from_user.first_name
    context.bot.send_message(chat_id=update.message.chat_id, text=response)
