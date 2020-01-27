import logging
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, \
    Filters, Updater, ConversationHandler, CallbackQueryHandler
import secrets
import model
import rsvp
import create_event

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
        return rsvp.start(update, context)

    else:
        create_event.start(update, context)


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


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],

    states={
        rsvp.COMING_OR_NOT: [CallbackQueryHandler(rsvp.coming_or_not)],
        rsvp.WHAT_TO_BRING: [CallbackQueryHandler(rsvp.what_to_bring)],
        rsvp.FINISH: [CallbackQueryHandler(rsvp.finish)],

    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

dispatcher.add_handler(create_event.create_event_handler)
dispatcher.add_handler(CommandHandler('attend', get_participants))
dispatcher.add_handler(conv_handler)

logger.info("* Start polling...")
updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
