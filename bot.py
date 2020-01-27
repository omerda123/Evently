import logging
import uuid
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, \
    Filters, Updater, ConversationHandler
import secrets
import model

DBNAME = "evently"

events_collection = model.get_collection(DBNAME, "events")
user_events_collection = model.get_collection(DBNAME, "user_events")

logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater(token=secrets.BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    if context.args:
        my_event = model.get_event(events_collection, context.args[0])
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
                             text=" Event created ! share the following message with your friends to RSVP You are invited to:")
    context.bot.send_message(chat_id=chat_id,
                             text=f"You are invited to {text} click here to RSVP:  t.me/event_handler_bot?start={event_id}")
    context.bot.send_message(chat_id=chat_id,
                             text="if you want to tell your friend to bring items to your party!")
    model.add_event(events_collection, event_id, text)
    model.add_event_to_user(user_events_collection, chat_id, event_id)
    return GET_ITEMS


def get_items(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> create event #{chat_id}")
    event_id = model.get_last_event(user_events_collection, chat_id)
    item = update.message.text
    model.add_items_to_event(events_collection, event_id, item)
    context.bot.send_message(chat_id=chat_id,
                             text=f"item {item} added to the list!")


def get_participants(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> create event #{chat_id}")
    event_id = model.get_last_event(user_events_collection, chat_id)
    participants = model.get_participants(events_collection, event_id)
    if participants:
        for participant in participants:
            context.bot.send_message(chat_id=chat_id, text=f"{participant['name'] : participant['rsvp']} ")
    else:
        context.bot.send_message(chat_id=chat_id, text="No friends attend yet")


def cancel(args):
    pass


def event(update: Update, context: CallbackContext):
    print(context.args)
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=context.args[0])

    # for arg in args:


CREATION, EVENT_CREATED, GET_ITEMS = range(3)

create_event_handler = ConversationHandler(

    entry_points=[CommandHandler('create_event', create_event)],

    states={
        CREATION: [MessageHandler(Filters.text, create_event)],

        EVENT_CREATED: [MessageHandler(Filters.text, event_created)],
        GET_ITEMS: [MessageHandler(Filters.text, get_items)],
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(create_event_handler)
dispatcher.add_handler(CommandHandler('attend', get_participants))

logger.info("* Start polling...")
updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
