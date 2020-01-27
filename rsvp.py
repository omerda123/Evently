import logging

import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, \
    Filters, Updater, CallbackQueryHandler, ConversationHandler
import secrets
import model
import bot
import create_event
DBNAME = "evently"


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
    info_about_event = model.get_event(events_collection, context.args[0])
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
    welcome_message = 'Hi, {} {} wants to know if you attend:{}'.format(user_name,'user_create_event', 'info_about_event[''description'']')
    update.message.reply_text(welcome_message, reply_markup=reply_markup)
    return COMING_OR_NOT


COMING_OR_NOT, WHAT_TO_BRING, FINISH = range(3)
list_of_stuff = ['bisly', 'cake', 'beer']


def coming_or_not(update: Update, context: CallbackContext):
    print("Hello")
    query = update.callback_query
    chat_id = update.effective_chat.id
    name = update.effective_user.first_name
    goodbye_massege = 'sorry to here your not coming {}, hope i see you soon'.format(name)
    coming_massege = "see you soon {}, you will arrive as:{} pepole\n what would like to bring?".format(name, query.data)
    if query.data == '0':
        context.bot.send_message(chat_id=chat_id, text=goodbye_massege)
    else:
        keyboard = []
        for item in list_of_stuff:
            print('hi')
            keyboard.append([InlineKeyboardButton(item, callback_data=item)])
        context.bot.send_message(chat_id=chat_id, reply_markup=InlineKeyboardMarkup(keyboard), text=coming_massege)
        return WHAT_TO_BRING


def what_to_bring(update, context):
    user_id = update.effective_chat.id
    what_user_bring = update.callback_query
    print(what_user_bring.data)
    print(user_id)


def finish():
    pass


def respond(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text
    logger.info(f"= Got on chat #{chat_id}: {text!r}")
    response = update.message.from_user.first_name
    context.bot.send_message(chat_id=update.message.chat_id, text=response)


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],

    states={
        COMING_OR_NOT: [CallbackQueryHandler(coming_or_not)],
        WHAT_TO_BRING: [CallbackQueryHandler(what_to_bring)],
        FINISH: [CallbackQueryHandler(finish)],

            },
    fallbacks=[CommandHandler('cancel', cancel)]
)
