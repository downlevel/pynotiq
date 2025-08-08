# PyNotiQ
A Python-powered queue-based notification system for Telegram

## Description
PyNotiQ is a lightweight and efficient Python application that reads messages from a queue and sends real-time notifications via Telegram. Built with the PyQueue client library, it supports both local and remote queue management. Perfect for alerting systems, deal tracking, and automated messaging.

## ✨ Features
- ✅ **Local & Remote Queue Support** - Works with both local files and remote PyQueue servers
- ✅ **Telegram Integration** - Sends notifications via Telegram Bot API
- ✅ **PyQueue Client** - Built on the robust PyQueue client library
- ✅ **Flexible Configuration** - Environment variables + command-line arguments
- ✅ **Message Tracking** - Prevents duplicate messages with sent status tracking
- ✅ **Multiple Queue Types** - Support for different queue configurations
- ✅ **Error Handling** - Robust error handling and retry logic
- ✅ **Easy Automation** - Perfect for scheduled tasks and automation workflows

## 🚀 Installation

1. Clone the repository:
```powershell
git clone https://github.com/downlevel/pynotiq.git
cd pynotiq
```

2. Install required dependencies:
```powershell
pip install -r requirements.txt
```

3. Set up your Telegram bot:
   - Create a bot with [@BotFather](https://t.me/botfather) on Telegram
   - Get your bot token
   - Get your chat ID (you can use [@userinfobot](https://t.me/userinfobot))

## 📁 Project Structure

```
pynotiq/
├── pynotiq.py              # Main application script
├── config.py               # Configuration management
├── test.py                 # Simple testing utility
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── queue.json             # Local queue file (auto-created)
└── README.md              # This file
```

### Key Files
- **`pynotiq.py`** - Main script that processes the queue and sends Telegram messages
- **`config.py`** - Handles configuration from environment variables
- **`test.py`** - Simple test script for adding messages to queue
- **`.env`** - Your configuration file (you need to create this)

## ⚙️ Configuration

### Method 1: Environment Variables (Recommended)
Create a `.env` file in the project directory:
```env
# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Queue Configuration
QUEUE_FILE_PATH=queue.json
PYQUEUE_QUEUE_TYPE=local
PYQUEUE_QUEUE_NAME=my-queue
PYQUEUE_SERVER_URL=http://localhost:8000
PYQUEUE_API_KEY=your_api_key_here
```

### Queue Types
- **Local Queue**: Uses local JSON file for message storage
- **Remote Queue**: Connects to a PyQueue server for distributed queue management

### Method 2: Command Line Arguments
```powershell
# Basic usage with local queue
python pynotiq.py -t your_bot_token -c your_chat_id

# Remote queue configuration
python pynotiq.py -qt remote -qs http://your-server:8000 -qn your-queue-name -qk your_api_key
```

## 📖 Usage

### Basic Usage
```powershell
# Process queue with default configuration
python pynotiq.py
```

### Advanced Usage
```powershell
# Local queue with custom file
python pynotiq.py -qt local -qf my_messages.json

# Remote queue
python pynotiq.py -qt remote -qs http://localhost:8000 -qn notifications

# Override Telegram credentials
python pynotiq.py -t YOUR_BOT_TOKEN -c YOUR_CHAT_ID

# Complete configuration
python pynotiq.py -qt remote -qs http://myserver:8000 -qn alerts -t BOT_TOKEN -c CHAT_ID
```

### Command Line Options
- `-qt, --queue-type`: Queue type (`local` or `remote`)
- `-qs, --queue-server`: Queue server URL (for remote queues)
- `-qk, --queue-api-key`: API key for PyQueue server
- `-qn, --queue-name`: Queue name
- `-qf, --queue`: Queue file path (for local queues)
- `-t, --token`: Telegram bot token
- `-c, --chatid`: Telegram chat ID
- `-h, --help`: Show help message

## 📦 Dependencies

- **requests** - HTTP client for Telegram Bot API
- **python-dotenv** - Environment variable management
- **pyqueue-client** - Queue management client library

## 📋 Message Format

PyNotiQ uses the PyQueue client library for message management. Messages should follow this structure:

```json
{
    "id": "unique-message-id",
    "timestamp": "2025-08-05T14:30:00.000000",
    "message_body": {
        "message_text": "📢 *Your notification message*\n💰 Price: €48.00\n🔗 [Link](https://example.com)",
        "sent": false,
        "message_type": "alert"
    }
}
```

### Message Properties
- `id`: Unique identifier for the message (UUID recommended)
- `timestamp`: ISO format timestamp when message was created
- `message_body.message_text`: The actual message text (supports Telegram Markdown)
- `message_body.sent`: Boolean indicating if message was sent (auto-managed)
- `message_body.send_date`: When the message was sent (auto-added)
- `message_body.message_type`: Optional categorization (alert, deal, report, etc.)

## 🔄 How It Works

1. **Initialize**: PyNotiQ connects to the specified queue (local or remote) using PyQueue client
2. **Fetch Messages**: Retrieves all messages from the queue using `queue.get_messages()`
3. **Filter Unsent**: Processes only messages where `sent` is `false` or missing
4. **Send to Telegram**: Uses Telegram Bot API to send each message
5. **Update Status**: Marks messages as sent and adds send timestamp
6. **Update Queue**: Uses `queue.update_message()` to persist the sent status

## 🧪 Testing

PyNotiQ includes multiple test utilities to help you validate your setup:

### Quick Testing with test.py
```powershell
# Add a single test message
python test.py

# Add multiple test messages
python test.py multiple
```

### Advanced Testing with test_pyqueue_client.py
```powershell
# Add a single test message (using pyqueue-client)
python test_pyqueue_client.py

# Add custom message
python test_pyqueue_client.py add -m "Hello from PyNotiQ!"

# Add multiple test messages
python test_pyqueue_client.py bulk -n 5

# View current queue
python test_pyqueue_client.py view
```

### Complete Test Workflow
1. Add test messages: `python test.py multiple`
2. Process messages: `python pynotiq.py`
3. Check your Telegram for received messages

## 📝 Examples

### Example 1: Basic Alert
```json
{
    "id": "alert_001",
    "timestamp": "2025-08-09T10:30:00.000000",
    "message_body": {
        "message_text": "🚨 System Alert: Server CPU usage is above 90%",
        "sent": false,
        "message_type": "alert"
    }
}
```

### Example 2: Deal Notification (with Markdown)
```json
{
    "id": "deal_123",
    "timestamp": "2025-08-09T14:15:30.000000",
    "message_body": {
        "message_text": "📢 *New Deal Found!*\n💰 *Price:* €25.00\n🎯 *Target:* €50.00\n🔗 [View Item](https://example.com/item/123)",
        "sent": false,
        "message_type": "deal"
    }
}
```

### Example 3: Daily Report
```json
{
    "id": "report_001",
    "timestamp": "2025-08-09T09:00:00.000000",
    "message_body": {
        "message_text": "📊 *Daily Report*\n• Sales: €1,250\n• Orders: 45\n• New customers: 12\n• System uptime: 99.9%",
        "sent": false,
        "message_type": "report"
    }
}
```

## 🔧 Automation

### Windows Task Scheduler
Run PyNotiQ every 5 minutes:
```powershell
schtasks /create /tn "PyNotiQ" /tr "python C:\path\to\pynotiq.py" /sc minute /mo 5
```

### Linux Cron Job
Add to crontab for every 5 minutes:
```bash
*/5 * * * * cd /path/to/pynotiq && python pynotiq.py
```

### Docker Integration
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "pynotiq.py"]
```

## 🛡️ Error Handling

- **Connection Failures**: Messages remain in queue for retry on next run
- **Invalid Messages**: Skipped with error logging, other messages continue processing
- **Missing Configuration**: Falls back to environment variables and config defaults
- **PyQueue Errors**: Graceful handling of queue client connection issues
- **Telegram API Errors**: Failed messages remain unmarked for retry

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
