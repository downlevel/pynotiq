import json
import requests
import os
from dotenv import load_dotenv
import argparse
import datetime
from pyqueue_client import PyQueue
from config import config 

load_dotenv()

parser = argparse.ArgumentParser(description="PyNotiQ Configuration")
parser.add_argument("-qt", "--queue-type", default=config.PYQUEUE_QUEUE_TYPE, help="Queue type( local or remote)")
parser.add_argument("-qs", "--queue-server", default=config.PYQUEUE_SERVER_URL, help="Queue server URL(leave empty for local queue)")
parser.add_argument("-qn", "--queue-name", default=config.PYQUEUE_QUEUE_NAME, help="Queue name")
parser.add_argument("-qf", "--queue", default=config.QUEUE_FILE_PATH, help="Queue file path")
parser.add_argument("-t", "--token", default=config.TELEGRAM_BOT_TOKEN, help="Bot Token")
parser.add_argument("-c", "--chatid", default=config.TELEGRAM_CHAT_ID, help="Chat ID")

args = parser.parse_args()

def send_telegram_message(message):

    url = f"https://api.telegram.org/bot{args.token}/sendMessage"
    payload = {
        "chat_id": args.chatid,
        "text": message
    }
    response = requests.post(url, json=payload)
    return response.status_code == 200

def process_queue():

    queue = PyQueue(
            server_url=args.queue_server,
            queue_type=args.queue_type,
            queue_name=args.queue_name
        )
    
    print("Processing queue")

    # Load data from queue
    messages = queue.get_messages()
    
    print(f"Messages in queue: {len(messages)}")
    for msg in messages:
        if "sent" not in msg["message_body"] or not msg["message_body"]["sent"]:  # Only process unsent messages
            if send_telegram_message(msg["message_body"]["message_text"]):
                msg["message_body"]["sent"] = True  # Mark as sent
                msg["message_body"]["send_date"] = str(datetime.datetime.now())
                print(f"Message sent: {msg['message_body']['message_text']}")
            else:
                print(f"Failed to send: {msg['message_body']['message_text']}")

            queue.update_message(msg)  # Update the message in the queue

if __name__ == "__main__":
    process_queue()
