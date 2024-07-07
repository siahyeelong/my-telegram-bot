# My Telegram Bots

This repo contains the telegram bots that I have created. Currently, there are 2 projects in this repo:
1. [Word of the week Bot](#word-of-the-week-telegram-bot)
1. [Chat with me Bot](#chat-with-me-telegram-bot)

This README contains instructions of how you can clone and run the bot for your own use if you so wish to

---


## Word of the week Telegram Bot
This is a Telegram bot that schedules a message every Monday at 6 AM to tell you the word of the week, including the definition and 3 examples of how to use it in a sentence. This project is created in Python.

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
Create a file `keys.py` to insert the relevant `TOKEN` and `CHAT_ID` variables.

Run the main program:
```bash
python word_of_the_week/main.py
```

## Chat with me Telegram Bot
This is a Telegram bot that represents me and allows people to ask about my personal, professional, or educational life. It uses the OpenAI API with OpenAI's Assistants to reply queries sent by the user. Since it uses the API, I have also limited each user's queries to 10 per user such that I will not go broke from servicing queries. This is done using a MySQL database to keep track of each user's conversation thread and query count.

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
    1. `TOKEN` (Telegram Bot Token)
    1. `OPENAI_TOKEN`
    1. `OPENAI_ASSISTANT_ID`
    1. `SQL_DATABASE_NAME`
    1. `SQL_DATABASE_PASSWORD`
    1. `SQL_TABLE_NAME`
1. Customise your own `SYSTEM_PROMPT` in `configs.py` (optional)
1. Run the main program:
    ```bash
    python chat_with_me/main.py
    ```