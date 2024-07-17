#!/bin/bash
echo starting script...
# Start MySQL server (replace with your MySQL server startup command)
sudo systemctl start mysql

# Function to create and manage screens
run_in_screen() {
    screen_name="$1"
    python_interpreter="$2"
    python_script="$3"
    
    # Create a new screen with the given name
    screen -dmS "$screen_name"
    
    # Send commands to the screen session
    screen -S "$screen_name" -X stuff "$python_interpreter $python_script$(printf '\r')"
}

# Activate virtual environment and run scripts

# Start 'wotw_bot' screen and run Python script
source /home/yl/Desktop/my-telegram-bot/venv/bin/activate
run_in_screen "wotw_bot" "/home/yl/Desktop/my-telegram-bot/venv/bin/python3" "/home/yl/Desktop/my-telegram-bot/word_of_the_week/main.py"

# Detach from virtual environment
deactivate

# Start 'chat_with_me_bot' screen and run Python script
source /home/yl/Desktop/my-telegram-bot/venv/bin/activate
run_in_screen "chat_with_me_bot" "/home/yl/Desktop/my-telegram-bot/venv/bin/python3" "/home/yl/Desktop/my-telegram-bot/chat_with_me/main.py"

# Detach from virtual environment
deactivate
echo script started...
