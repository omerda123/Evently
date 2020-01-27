import logging
import uuid
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, \
    Filters, Updater, ConversationHandler

import secrets
import model

logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater(token=secrets.BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    if context.args:
        my_event = model.get_event(context.args[0])
        context.bot.send_message(chat_id=chat_id,
                                 text=my_event["description"])

    else:

        context.bot.send_message(chat_id=chat_id,
                                 text=""" Welcome! 💣
            Hi, to create a event please type /create_event
                                                       """)


def create_event(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> create event #{chat_id}")
    context.bot.send_message(chat_id=chat_id,
                             text="""Please enter all info about the event below in one line:
            example: Joe's birthday picnic 2/2/2020, 17:00, Jabotinsky 25 Tel Aviv you can park at Arlozorov parking""")
    return EVENT_CREATED


def event_created(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> create event #{chat_id}")
    text = update.message.text
    event_id = str(uuid.uuid1())
    context.bot.send_message(chat_id=chat_id,
                             text=f""" Event created ! share the following message with your friends to RSVP You are invited to:
{text}
click here to RSVP:  t.me/event_handler_bot?start={event_id}
if you want to tell your friend items to bring please write /add_list
""")

    model.add_event(event_id,text)
    return ConversationHandler.END


def get_items(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> create event #{chat_id}")
    context.bot.send_message(chat_id=chat_id,
                             text="""please write the stuff you need for the event followed by #end""")


def insert_items(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> create event #{chat_id}")
    context.bot.send_message(chat_id=chat_id,
                             text="""item inserted""")
    return GET_ITEMS


def cancel(args):
    pass


def event(update: Update, context: CallbackContext):
    print(context.args)
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=context.args[0])

    # for arg in args:


CREATION, EVENT_CREATED, = range(2)
GET_ITEMS, INSERT_ITEMS = range(2)

create_event_handler = ConversationHandler(

    entry_points=[CommandHandler('create_event', create_event)],

    states={
        CREATION: [MessageHandler(Filters.text, create_event)],

        EVENT_CREATED: [MessageHandler(Filters.text, event_created)],
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

add_item_handler = ConversationHandler(

    entry_points=[CommandHandler('add_list', get_items)],

    states={
        GET_ITEMS: [MessageHandler(Filters.text, get_items)],

        INSERT_ITEMS: [MessageHandler(Filters.text, insert_items)],
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(create_event_handler)
dispatcher.add_handler(add_item_handler)
dispatcher.add_handler(CommandHandler('event', event, pass_args=True))

logger.info("* Start polling...")
updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
