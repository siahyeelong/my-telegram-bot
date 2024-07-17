from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler
from keys import TELEGRAM_TOKEN, MAIN_CHAT_ID
from sql_backend import SQL_Database

from datetime import time
import pytz
timezone = pytz.timezone('Asia/Singapore')

import pandas as pd
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_filename: str = os.path.join(current_dir,"words.csv")
df = pd.read_csv(csv_filename)

# Logging set up
from logger import setup_logger
logger = setup_logger()

# Function that gets and formats the new word of the week
def get_wotw() -> str:
    global df
    for row in df.values:
        if row[5]=='no':
            row[5]='yes'
            df.to_csv(csv_filename, index=False)
            return f"{row[0]}\n\n{row[1]}\n\n{row[2]}\n{row[3]}\n{row[4]}"
    return "No more words left to teach you!"

# Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    database = SQL_Database()
    database.insert_new_chat_id(update.message.chat.id, update.message.chat.username)
    await update.message.reply_text("welcome! you have just been subscribed to the weekly word-of-the-week message! if you wish to unsubscribe, just /unsubscribe")
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("this bot sends you a new word + its definition + 3 uses in a sentence every Monday at 6am. have fun learning!\n\n/start -- enrol in the weekly scheduled message\n/unsubscribe -- unsubscribe from the weekly message")
    
async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    database = SQL_Database()
    database.delete_record(update.message.chat.id)
    await update.message.reply_text("you have been unsubscribed. hope you had fun learning!")

async def scheduled_messager(context: ContextTypes.DEFAULT_TYPE):       
    wotw = get_wotw()
    database = SQL_Database()
    ID_list = database.get_all_records()
    for ID in ID_list:
        logger.debug(f"sending {ID[0]} / {ID[1]} the message...")
        await context.bot.send_message(chat_id=ID[0], text=wotw)
    
async def error_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Update {update} caused error: {context.error}")

if __name__=="__main__":
    logger.info("bot has started...")
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    job_queue = application.job_queue

    # Schedule the job to run at 6 AM every Monday
    job_minute = job_queue.run_daily(callback=scheduled_messager,                    # the callback function
                                     time=time(hour=6, minute=3, tzinfo=timezone),   # 6:03am
                                     days=(2,))                                      # Tuesday is represented by 2

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe_command))
    application.add_error_handler(error_message)
    
    application.run_polling(poll_interval=2)