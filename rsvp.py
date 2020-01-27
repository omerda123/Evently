import logging

import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, \
    Filters, Updater, CallbackQueryHandler, ConversationHandler
import secrets
import model

DBNAME = "evently"

import secrets

event_id = {"id": ""}
guest_info = {"brings": []}

COMING_OR_NOT, WHAT_TO_BRING, FINISH = range(3)

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
    info_about_event = model.get_event(events_collection, event_id['id'])
    list_of_stuff = info_about_event['items']
    query = update.callback_query
    guest_info['num_of_participants'] = query.data
    chat_id = update.effective_chat.id
    name = update.effective_user.first_name
    coll = model.get_collection(DBNAME, 'events')
    model.rsvp(coll, event_id['id'], chat_id, name, guest_info['num_of_participants'])
    goodbye_massege = 'sorry to here your not coming {}, hope i see you soon'.format(name)
    coming_massege = "see you soon {}, you will arrive as:{} pepole\n what would like to bring?".format(name,
                                                                                                        guest_info[
                                                                                                            'num_of_participants'])
    if query.data == '0':
        context.bot.send_message(chat_id=chat_id, text=goodbye_massege)
    else:
        keyboard = [[InlineKeyboardButton("i dont want to bring anything, thanks", callback_data='no')]]
        for item in list_of_stuff:
            print('hi')
            keyboard.append([InlineKeyboardButton(item, callback_data=item)])
        context.bot.send_message(chat_id=chat_id, reply_markup=InlineKeyboardMarkup(keyboard), text=coming_massege)

        return WHAT_TO_BRING


def what_to_bring(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    info_about_event = model.get_event(events_collection, event_id['id'])
    list_of_stuff = info_about_event['items']
    info_about_event = model.get_event(events_collection, event_id['id'])
    list_of_stuff = info_about_event['items']
    print(list_of_stuff)
    print(guest_info['brings'])
    if guest_info['brings'] != 'no':
        keyboard = [[InlineKeyboardButton("i dont want to bring anything, thanks", callback_data='no')]]
        for item in list_of_stuff:
            keyboard.append([InlineKeyboardButton(item, callback_data=item)])
        next_massege = 'you choose to brings {}, do you want to bring another things?'.format(guest_info['brings'])
        context.bot.send_message(chat_id=chat_id, reply_markup=InlineKeyboardMarkup(keyboard), text=next_massege)

    coll = model.get_collection(DBNAME, 'events')
    user_id = update.effective_chat.id
    query = update.callback_query
    model.friend_brings_item(coll, event_id['id'], user_id, query.data)


def finish():
    pass


def respond(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text
    logger.info(f"= Got on chat #{chat_id}: {text!r}")
    response = update.message.from_user.first_name
    context.bot.send_message(chat_id=update.message.chat_id, text=response)
