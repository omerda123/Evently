from telegram.ext import CommandHandler, CallbackContext, MessageHandler, \
    Filters, Updater, ConversationHandler
from telegram import Update
import uuid
import model

DBNAME = "evently"
events_collection = model.get_collection(DBNAME, "events")
user_events_collection = model.get_collection(DBNAME, "user_events")

CREATION, EVENT_CREATED, GET_ITEMS = range(3)


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id,
                             text=""" Welcome! 💣
        Hi, to create a event please type /create_event
                                                   """)


def create_event(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id,
                             text="""Please enter all info about the event below in one line:
            example: Joe's birthday picnic 2/2/2020, 17:00, Jabotinsky 25 Tel Aviv you can park at Arlozorov parking""")
    return EVENT_CREATED


def event_created(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text
    event_id = str(uuid.uuid1())
    context.bot.send_message(chat_id=chat_id,
                             text=" Event created ! share the following message with your friends to RSVP You are invited to:")
    context.bot.send_message(chat_id=chat_id,
                             text=f"You are invited to {text} click here to RSVP:  t.me/event_handler_bot?start={event_id}")
    context.bot.send_message(chat_id=chat_id,
                             text="if you want to tell your friend to bring items to your party!")
    print(update.effective_chat)
    name = f"{update.effective_chat['first_name']} {update.effective_chat['last_name']}"
    model.add_event(events_collection, event_id, text, name)
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


def cancel(args):
    pass


create_event_handler = ConversationHandler(

    entry_points=[CommandHandler('create_event', create_event)],

    states={
        CREATION: [MessageHandler(Filters.text, create_event)],
        EVENT_CREATED: [MessageHandler(Filters.text, event_created)],
        GET_ITEMS: [MessageHandler(Filters.text, get_items)],
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)
