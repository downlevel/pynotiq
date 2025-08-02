# PyNotiQ
A Python-powered queue-based notification system for Telegram

## Description
PyNotiQ is a lightweight and efficient Python application that reads messages from a queue and sends real-time notifications via Telegram. Perfect for alerting systems, deal tracking, and automated messaging.

## ✨ Features
- ✅ Reads from JSON queue
- ✅ Sends notifications via Telegram
- ✅ Lightweight & easy to configure
- ✅ Ideal for automation and alerts
- ✅ Environment variable support
- ✅ Command-line argument support
- ✅ Message tracking (prevents duplicates)

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pynotiq.git
cd pynotiq
```

2. Install required dependencies:
```bash
pip install requests python-dotenv
```

3. Set up your Telegram bot:
   - Create a bot with [@BotFather](https://t.me/botfather) on Telegram
   - Get your bot token
   - Get your chat ID (you can use [@userinfobot](https://t.me/userinfobot))

## ⚙️ Configuration

### Method 1: Environment Variables (Recommended)
Create a `.env` file in the project directory:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
QUEUE_FILE=queue.json
```

### Method 2: Command Line Arguments
```bash
python pynotiq.py -t your_bot_token -c your_chat_id -q queue.json
```

## 📖 Usage

### Basic Usage
```bash
python pynotiq.py
```

### With Command Line Arguments
```bash
# Specify custom queue file
python pynotiq.py --queue my_messages.json

# Override bot token and chat ID
python pynotiq.py --token YOUR_BOT_TOKEN --chatid YOUR_CHAT_ID

# All options together
python pynotiq.py -t YOUR_BOT_TOKEN -c YOUR_CHAT_ID -q custom_queue.json
```

### Command Line Options
- `-q, --queue`: Queue file path (default: queue.json)
- `-t, --token`: Telegram bot token
- `-c, --chatid`: Telegram chat ID
- `-h, --help`: Show help message

## 📋 Queue File Format

The queue file should be a JSON array containing message objects. Each message should have:

```json
[
    {
        "Id": "unique_message_id",
        "Timestamp": "2025-03-06T20:17:38.440609",
        "MessageBody": "📢 *Your notification message*\n💰 Price: €48.00\n🔗 [Link](https://example.com)"
    },
    {
        "Id": "another_message_id", 
        "Timestamp": "2025-03-06T20:20:15.123456",
        "MessageBody": "🚨 Alert: Something important happened!"
    }
]
```

### Message Properties
- `Id`: Unique identifier for the message
- `Timestamp`: When the message was created
- `MessageBody`: The actual message text (supports Markdown formatting)
- `sent`: (Auto-added) Boolean indicating if message was sent
- `send_date`: (Auto-added) When the message was sent

## 🔄 How It Works

1. PyNotiQ reads the queue file specified (default: `queue.json`)
2. Processes all unsent messages in the queue
3. Sends each message to your Telegram chat
4. Marks messages as sent to prevent duplicates
5. Updates the queue file with sent status and timestamps

## 📝 Examples

### Example 1: Basic Alert
```json
[
    {
        "Id": "alert_001",
        "Timestamp": "2025-08-02T10:30:00.000000",
        "MessageBody": "🚨 System Alert: Server CPU usage is above 90%"
    }
]
```

### Example 2: Deal Notification (with Markdown)
```json
[
    {
        "Id": "deal_123",
        "Timestamp": "2025-08-02T14:15:30.000000", 
        "MessageBody": "📢 *New Deal Found!*\n💰 *Price:* €25.00\n🎯 *Target:* €50.00\n🔗 [View Item](https://example.com/item/123)"
    }
]
```

### Example 3: Multiple Messages
```json
[
    {
        "Id": "msg_001",
        "Timestamp": "2025-08-02T09:00:00.000000",
        "MessageBody": "☀️ Good morning! Daily backup completed successfully."
    },
    {
        "Id": "msg_002", 
        "Timestamp": "2025-08-02T09:05:00.000000",
        "MessageBody": "📊 Yesterday's stats:\n• Sales: €1,250\n• Orders: 45\n• New customers: 12"
    }
]
```

## 🔧 Automation

### Windows Task Scheduler
Run PyNotiQ every 5 minutes:
```bash
schtasks /create /tn "PyNotiQ" /tr "python C:\path\to\pynotiq.py" /sc minute /mo 5
```

### Linux Cron Job
Add to crontab for every 5 minutes:
```bash
*/5 * * * * cd /path/to/pynotiq && python pynotiq.py
```

## 🛡️ Error Handling

- Messages that fail to send remain unmarked and will be retried on next run
- Invalid queue files are safely ignored
- Missing environment variables can be overridden with command line arguments

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
