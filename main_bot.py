from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler
from keys import TOKEN, CHAT_ID

from datetime import time
import pytz
timezone = pytz.timezone('Asia/Singapore')

import pandas as pd
csv_filename: str = "words.csv"
df = pd.read_csv(csv_filename)

# Logging set up
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

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
    await update.message.reply_text("hello! bot has started!")
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("this bot sends you a new word + its definition + 3 uses in a sentence every Monday at 6am. have fun learning!")

async def scheduled_messager(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=CHAT_ID, text=get_wotw())
    
async def error_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Update {update} caused error: {context.error}")


if __name__=="__main__":
    logger.info("bot has started...")
    
    application = Application.builder().token(TOKEN).build()
    job_queue = application.job_queue

    # Schedule the job to run at 6 AM every Monday
    job_minute = job_queue.run_daily(scheduled_messager,                    # the callback function
                                     time=time(6, 0, 0, tzinfo=timezone),   # 6am
                                     days=(0,))                             # Monday is represented by 0

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_error_handler(error_message)
    
    application.run_polling(poll_interval=2)