import json
import requests
import os
from dotenv import load_dotenv
import argparse
import datetime

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
QUEUE_FILE = os.getenv("QUEUE_FILE")

parser = argparse.ArgumentParser(description="PyNotiQ Configuration")
parser.add_argument("-q", "--queue", default="queue.json", help="Queue file")
parser.add_argument("-t", "--token", help="Bot Token")
parser.add_argument("-c", "--chatid", help="Chat ID")

args = parser.parse_args()

if args.token:
    TELEGRAM_BOT_TOKEN = args.token
if args.chatid:
    TELEGRAM_CHAT_ID = args.chatid
if args.queue:
    QUEUE_FILE = args.queue

def send_telegram_message(message):

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, json=payload)
    return response.status_code == 200

def process_queue():

    print("Processing queue...")
    print(f"Queue file: {QUEUE_FILE}")

    if not os.path.exists(QUEUE_FILE):
        return  # No messages in queue

    with open(QUEUE_FILE, "r") as f:
        queue = json.load(f)

    print(f"Messages in queue: {len(queue)}")
    for msg in queue:
        if "sent" not in msg or not msg["sent"]:  # Only process unsent messages
            if send_telegram_message(msg["MessageBody"]):
                msg["sent"] = True  # Mark as sent
                msg["send_date"] = str(datetime.datetime.now())
                print(f"Message sent: {msg['MessageBody']}")
            else:
                print(f"Failed to send: {msg['MessageBody']}")

    # Save updated queue back to file
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=4)

if __name__ == "__main__":
    process_queue()
