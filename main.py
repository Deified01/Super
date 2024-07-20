import asyncio
import os
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask
import threading 
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

def run_flask_app():
    app.run(host='0.0.0.0', port=10000)

# Set API ID, API hash, and session string
"""os.environ['id'] 
os.environ['hash']
os.environ['string']"""

api_id = int(os.environ['id'])
api_hash = os.environ['hash']
session_str = os.environ['string']

# Create a Telegram client
client = TelegramClient(StringSession(session_str), api_id, api_hash)

# Start the client
client.start()

# Define the functions to extract win/loss amounts
def extract_win_amount(message):
    pattern = r'You won ₩(\d+)'
    match = re.search(pattern, re.escape(message).replace(' ', '\ '))
    if match:
        return int(match.group(1))
    else:
        return None

def extract_loss_amount(message):
    pattern = r'You lost ₩(\d+)'
    match = re.search(pattern, re.escape(message).replace(' ', '\ '))
    if match:
        return int(match.group(1))
    else:
        return None

# Define a variable to store the current balance
balance = 500000000

# Define an event handler to process incoming messages
@client.on(events.NewMessage(chats=['@lustXcatcherrobot']))
async def handle_message(event):
    global balance
    message = event.message.message
    win_amount = extract_win_amount(message)
    loss_amount = extract_loss_amount(message)
    
    try:
        if win_amount:
            balance += win_amount
            print(f'Win amount: {win_amount}, New balance: {balance}')
        elif loss_amount:
            balance -= loss_amount
            print(f'Loss amount: {loss_amount}, New balance: {balance}')
        else:
            print('No win/loss amount found in message')
    except Exception as e:
        print(f'Error processing message: {e}')

# Define a function to send the lever command
async def send_lever_command():
    global balance
    while True:
        try:
            amount = int(balance * 0.4)
            await client.send_message('@lustXcatcherrobot', f'/lever {amount}')
            print(f'Sent lever command with amount {amount}')
            await asyncio.sleep(610)
        except Exception as e:
            print(f'Error sending lever command: {e}')
            await asyncio.sleep(10)  # wait 10 seconds before retrying

# Run the client and send the lever command
if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    client.loop.create_task(send_lever_command())
    client.run_until_disconnected()
