from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler, filters
from keys import TESTBOT_TOKEN
from chatgpt_assistant import GPT_assistant
from chat_with_me.sql_backend import SQL_Database
database = SQL_Database()

import pytz
timezone = pytz.timezone('Asia/Singapore')

# Logging set up
from logger import setup_logger
logger = setup_logger()

# Customised functions
def check_and_send(update: Update) -> str:
    '''
    This function logs a new user's chat, and allows a ChatGPT query to be sent only if the user has queried < 10 times
    '''
    id = update.message.chat.id
    username = update.message.chat.username
    question = update.message.text
    
    database.insert_new_chat_id(id)
    chat_count, max_count, threadID = database.get_row(id)
    if chat_count > max_count:
        logger.info(f"id:{id} username:{username} queried more than 10 times")
        return "sorry! you have queried more than 10 times, and since Yee Long is kinda broke, he can't service any more of your requests. if you would like to contact him directly, please do so @yeelong"
    elif max_count == 0:
        logger.error("max_count was 0 for some reason")
        return "oh no! something went wrong, screenshot this message and send it to @yeelong"
    else:
        database.increment_chat_count(id)
        assistant = GPT_assistant()
        assistant.set_thread(threadID)
        try:
            return assistant.ask_assistant(question)
        except Exception as e:
            logger.error(f"Something went wrong! id-{id}\ncount-{chat_count}\n{username} said: {question}\nError: {e}")
            return f"Something went wrong! id-{id}\ncount-{chat_count}\nYou said: {question}\nError: {e}"

# Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(update.message.chat_id)
    await update.message.reply_text("hi! I am Yee Long's AI assistant. he built me so that I can help you get to know him better. to begin, just type what you wanna ask about Yee Long in this chat.\ndo note that you are limited only to 10 queries")
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I am Yee Long's AI assistant and he has fed me with knowledge about him so that I can share it with you. simply ask me what you wanna know about him here.\nsome examples of what you can ask:\n1. what is your education background?\n2. what are your hobbies?\n3. are you available for an internship?")
    
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