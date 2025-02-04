import json
import requests
import os

TELEGRAM_BOT_TOKEN = "your-telegram-bot-token"
TELEGRAM_CHAT_ID = "your-chat-id"
QUEUE_FILE = "queue.json"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, json=payload)
    return response.status_code == 200

def process_queue():
    if not os.path.exists(QUEUE_FILE):
        return  # No messages in queue

    with open(QUEUE_FILE, "r") as f:
        queue = json.load(f)

    for msg in queue:
        if not msg["sent"]:  # Only process unsent messages
            if send_telegram_message(msg["message"]):
                msg["sent"] = True  # Mark as sent
                print(f"Message sent: {msg['message']}")
            else:
                print(f"Failed to send: {msg['message']}")

    # Save updated queue back to file
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=4)

if __name__ == "__main__":
    process_queue()
