# My Telegram Bots

This repo contains the telegram bots that I have created. Currently, there are 2 projects in this repo:
1. [Word of the week Bot](#word-of-the-week-telegram-bot)
1. [Chat with me Bot](#chat-with-me-telegram-bot)

This README contains instructions of how you can clone and run the bot for your own use if you so wish to

The bots are currently run on my home's Raspberry Pi 4. I have also included the startup script to start the bot upon reboot.

---


## Word of the week Telegram Bot
> *Try it out for yourself! Go to [@ylWOTWbot](https://t.me/ylWOTWbot) on Telegram and see my bot in action*

This is a Telegram bot that schedules a message every Monday at 6 AM to tell you the word of the week, including the definition and 3 examples of how to use it in a sentence. This project is created in Python.

I was inspired to create this bot as I wanted to add new words into my everyday vocabulary. Knowing that a daily "word of the day" would simply overwhelm me and make it seem like a chore to integrate it into my vocabulary, I decided to learn a new word every week instead. I also included figures of speech and idioms besides just single words. To help with the process, I ChatGPT-ed the examples listen in `words.csv` so that I know how to use the words / phrases in my sentences.

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/siahyeelong/my-telegram-bot.git
    cd my-telegram-bot
    ```
2. **Create and Activate a Virtual Environment**:
- **On Windows**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- **On macOS and Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Usage
Create a file `keys.py` to insert the relevant `TELEGRAM_TOKEN` and `MAIN_CHAT_ID` variables.

Run the main program:
```bash
cd word_of_the_week
python main.py
```

## Chat with me Telegram Bot
> *Try it out for yourself! Go to [@yltelebot](https://t.me/yltelebot) on Telegram and see my bot in action*

This is a Telegram bot that represents me and allows people to ask about my personal, professional, or educational life. It uses the OpenAI API with OpenAI's Assistants to reply queries sent by the user. Since it uses the API, I have also limited each user's queries to 10 per user such that I will not go broke from servicing queries. This is done using a MySQL database to keep track of each user's conversation thread and query count.

I was inspired to create this bot as I wanted people to know me better without actually having to talk to me. I found that this might be useful for potential recruiters too since they get a preview of who I am before interacting with me. 

While the bot currently runs an OpenAI API in the back, I am exploring local LLM compute, but am currently too broke to buy good-enough hardware for it.

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/siahyeelong/my-telegram-bot.git
    cd my-telegram-bot
    ```
2. **Create and Activate a Virtual Environment**:
- **On Windows**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- **On macOS and Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Usage
1. Ensure that you have a MySQL server running
1. Create a `keys.py` file to specify
    1. `TELEGRAM_TOKEN`
    1. `OPENAI_TOKEN`
    1. `OPENAI_ASSISTANT_ID`
    1. `SQL_DATABASE_NAME`
    1. `SQL_DATABASE_PASSWORD`
    1. `SQL_TABLE_NAME`
    1. `MAIN_CHAT_ID` (Admin's chat ID with the bot. You may find this at [@userinfobot](t.me/userinfobot) on Telegram)
1. Customise your own `SYSTEM_PROMPT` in `configs.py` (optional)
1. Run the main program:
    ```bash
    cd chat_with_me
    python main.py
    ```