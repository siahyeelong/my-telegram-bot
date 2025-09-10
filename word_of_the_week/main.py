from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler
from keys import TELEGRAM_TOKEN
from mongodb_backend import Database

from datetime import time
import pytz

timezone = pytz.timezone("Asia/Singapore")

# Logging set up
from logger import setup_logger

logger = setup_logger()
db = Database()


# Function that gets and formats the new word of the week
def get_wotw() -> str:
    word = db.get_word()
    if word is not None:
        return f"{word['word']}\n\n{word['definition']}\n\n{word['sentence1']}\n{word['sentence2']}\n{word['sentence3']}"
    else:
        return "No more words left to teach you!"


# Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    wotw = db.add_user(update.message.chat.username, str(update.message.chat.id))
    wotw = f"{wotw['word']}\n\n{wotw['definition']}\n\n{wotw['sentence1']}\n{wotw['sentence2']}\n{wotw['sentence3']}"
    await update.message.reply_text(
        "welcome! you have just been subscribed to the weekly word-of-the-week message! if you wish to unsubscribe, just /unsubscribe"
    )
    await update.message.reply_text(wotw)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "this bot sends you a new word + its definition + 3 uses in a sentence every Tuesday at 6am. have fun learning!\n\n/start -- enrol in the weekly scheduled message\n/unsubscribe -- unsubscribe from the weekly message"
    )


async def unsubscribe_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    db.remove_user(str(update.message.chat.id))
    logger.warning(f"{update.message.chat.username} has unsubscribed")
    await update.message.reply_text(
        "you have been unsubscribed. hope you had fun learning!"
    )


async def scheduled_messager(context: ContextTypes.DEFAULT_TYPE):
    wotw = get_wotw()
    for subscriber in db.users.find():
        if subscriber["chatid"] != "":
            logger.debug(
                f"sending user: {subscriber['username']} / chatid: {subscriber['chatid']} the message..."
            )
            await context.bot.send_message(chat_id=subscriber["chatid"], text=wotw)


async def error_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Update {update} caused error: {context.error}")


if __name__ == "__main__":
    logger.info("bot has started...")

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    job_queue = application.job_queue

    # Schedule the job to run at 6 AM every Tuesday
    job_minute = job_queue.run_daily(
        callback=scheduled_messager,  # the callback function
        time=time(hour=6, minute=3, tzinfo=timezone),  # 6:03am
        days=(2,),
    )  # Tuesday is represented by 2

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe_command))
    application.add_error_handler(error_message)

    application.run_polling(poll_interval=2)
