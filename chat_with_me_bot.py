from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler, filters
from keys import TESTBOT_TOKEN, CHAT_ID
#from chatgpt_query import ask_chatgpt
from sql_backend import SQL_Database
database = SQL_Database()

import json
from datetime import time
import pytz
timezone = pytz.timezone('Asia/Singapore')

# Logging set up
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

# Customised functions
def check_and_send(update: Update) -> str:
    '''
    this function allows a message to be sent only if the user has queried < 10 times
    '''
    id = update.message.chat.id
    database.insert_new_chat_id(id)
    chat_count, max_count = database.get_chat_and_max_count(id)
    if chat_count > max_count:
        return "simulate sent unsuccessfully"
    else:
        database.increment_chat_count(id)
        return f"successfully sent! id-{id} count-{chat_count}"

# Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(update.message.chat_id)
    await update.message.reply_text( "nothing" )
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("this bot sends you a new word + its definition + 3 uses in a sentence every Monday at 6am. have fun learning!")
    
async def error_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Update {update} caused error: {context.error}")
    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text: str = update.message.text
    
    logger.info(f"User ({update.message.chat.id}) said '{text}'")
    
    response: str = check_and_send(update)
    
    logger.info("bot says:", response)
    await update.message.reply_text(response)


if __name__=="__main__":
    logger.info("bot has started...")
    
    application = Application.builder().token(TESTBOT_TOKEN).build()
    job_queue = application.job_queue

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    application.add_error_handler(error_message)
    
    application.run_polling()