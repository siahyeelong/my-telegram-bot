from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext
from keys import TELEGRAM_TOKEN, MAIN_CHAT_ID
from chatgpt_assistant import GPT_assistant
from sql_backend import SQL_Database
database = SQL_Database()

import pytz
timezone = pytz.timezone('Asia/Singapore')

# Logging set up
from logger import setup_logger
logger = setup_logger()

# Customised functions
async def check_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
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
        await handle_exceeded_queries(update, context) # fix this part. when the programme reaches here, a message should be sent to a specific chatid
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
    
    response: str = await check_and_send(update, context)
    
    logger.info(f"bot says: {response}")
    await update.message.reply_text(response)

async def handle_exceeded_queries(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = f"@{update.message.chat.username} wants more queries. Grant 10 more or reject?"
    
    keyboard = [
        [
            InlineKeyboardButton("Grant", callback_data='grant'),
            InlineKeyboardButton("Reject", callback_data='reject'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(chat_id=MAIN_CHAT_ID, text=text, reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    chosen = query.data
    chat_id = query.message.chat.id
    username = query.message.chat.username
    
    if chosen == 'grant':
        # Reset chat_count to 0
        database.reset_chat_count(chat_id)
        await query.edit_message_text(text=f"you have granted @{username} 10 more queries! yay!")
    else:
        await query.edit_message_text(text=f"you have rejected @{username} :((")

if __name__=="__main__":
    logger.info("bot has started...")
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    job_queue = application.job_queue

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    application.add_handler(CallbackQueryHandler(button))
    
    application.add_error_handler(error_message)
    
    application.run_polling()