from pymongo import MongoClient

from survey import insert_questions
import logging
import telegram
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, \
    Filters, Updater, ConversationHandler
import bot_settings

logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater(token=bot_settings.BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def cancel(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text="Goodbye")


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    custom_keyboard = ["כן", "לא"],
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(""" 
                             היי, האם תרצה להשתתף בסקר קצר לקראת הבחירות?
                               ניתן לצאת באמצעות /cancel
                           """,
                              reply_markup=reply_markup)

    return AGE


AGE, GENDER, CITY, PARTY, FINISH = range(5)


def age(update: Update, context: CallbackContext):
    text = update.message.text
    res["user_id"] = update.effective_chat.id
    res["name"] = update.effective_chat.first_name
    res["lname"] = update.effective_chat.last_name
    res["want"] = text

    custom_keyboard = ["18-30", "30-40", "40-50", "50-60"],
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text("בן כמה אתה?", reply_markup=reply_markup)
    return GENDER


def gender(update: Update, context: CallbackContext):
    text = update.message.text
    res["age"] = text

    custom_keyboard = ["זכר", "נקבה", "אחר"],
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text("מה המין שלך?", reply_markup=reply_markup)
    return CITY


def city(update: Update, context: CallbackContext):
    text = update.message.text
    res["gender"] = text
    update.message.reply_text("מהי עיר מגוריך?", reply_markup=ReplyKeyboardRemove())

    return PARTY


def party(update: Update, context: CallbackContext):
    text = update.message.text
    res["city"] = text
    custom_keyboard = ["ליכוד", "כחול לבן", "שס", "ימינה"],
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text("באיזה מפלגה את\ה מתכוון לבחור?",
                              reply_markup=reply_markup)

    return FINISH


def finish(update: Update, context: CallbackContext):
    text = update.message.text
    res["party"] = text
    client = MongoClient()
    db = client.get_database("survey")
    results = db.get_collection("results")
    results.insert_one(res)
    print(res)
    res.clear()
    custom_keyboard = ["/start" , "/cancel"],
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text("תודה רבה שהשתתפת.",
                              reply_markup=reply_markup)
    return ConversationHandler.END


conv_handler = ConversationHandler(

    entry_points=[CommandHandler('start', start)],

    states={
        AGE: [MessageHandler(Filters.text, age)],

        GENDER: [MessageHandler(Filters.text, gender)],

        CITY: [MessageHandler(Filters.text, city)],

        PARTY: [MessageHandler(Filters.text, party)],

        FINISH: [MessageHandler(Filters.text, finish)],
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)
dispatcher.add_handler(CommandHandler('cancel', cancel))
dispatcher.add_handler(conv_handler)
res = {}
logger.info("* Start polling...")
updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
