#!/usr/bin/env python3
"""
Simple test script for PyNotiQ - Test adding messages to queue
"""

import json
import datetime
import uuid
from pyqueue_client import PyQueue
from config import config

def test_add_message():
    """Test adding a single message to the queue"""
    print("🧪 Testing PyNotiQ - Add Message to Queue")
    print("=" * 50)
    
    # Initialize PyQueue with config defaults
    queue = PyQueue(
        server_url=config.PYQUEUE_SERVER_URL if config.PYQUEUE_SERVER_URL else None,
        queue_type=config.PYQUEUE_QUEUE_TYPE,
        queue_file=config.QUEUE_FILE_PATH,
        queue_name=config.PYQUEUE_QUEUE_NAME,
        api_key=config.PYQUEUE_API_KEY if config.PYQUEUE_API_KEY else None
    )
    
    # Display configuration
    print(f"Queue Type: {config.PYQUEUE_QUEUE_TYPE}")
    print(f"Queue Name: {config.PYQUEUE_QUEUE_NAME}")
    if config.PYQUEUE_SERVER_URL:
        print(f"Server URL: {config.PYQUEUE_SERVER_URL}")
    print()
    
    # Create test message
    test_message = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.now().isoformat(),
        "message_body": {
            "message_text": f"🧪 Test Message - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "sent": False,
            "message_type": "test"
        }
    }
    
    try:
        # Add message to queue
        print("Adding test message to queue...")
        result = queue.add_message(test_message)
        
        if result:
            print("✅ SUCCESS: Message added to queue!")
            print(f"📝 Message: {test_message['message_body']['message_text']}")
            print(f"🆔 Message ID: {test_message['id']}")
            
            # Verify message was added by getting messages
            print("\n🔍 Verifying message in queue...")
            messages = queue.get_messages()
            print(f"📊 Total messages in queue: {len(messages)}")
            
            # Find our test message
            found = any(msg['id'] == test_message['id'] for msg in messages)
            if found:
                print("✅ Message verified in queue!")
            else:
                print("❌ Message not found in queue!")
                
        else:
            print("❌ FAILED: Could not add message to queue")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        
    print("\n" + "=" * 50)
    print("💡 Next step: Run 'python pynotiq.py' to process the queue")

def test_add_multiple_messages():
    """Test adding multiple messages to the queue"""
    print("🧪 Testing PyNotiQ - Add Multiple Messages")
    print("=" * 50)
    
    # Initialize PyQueue
    queue = PyQueue(
        server_url=config.PYQUEUE_SERVER_URL,
        queue_type=config.PYQUEUE_QUEUE_TYPE,
        queue_name=config.PYQUEUE_QUEUE_NAME,
        queue_file=config.QUEUE_FILE_PATH,
        api_key=config.PYQUEUE_API_KEY
    )
    
    # Test messages
    test_messages = [
        ("🚨 Alert: High CPU usage detected", "alert"),
        ("💰 Deal: 50% off Python courses", "deal"),
        ("📊 Report: Daily backup completed", "report"),
        ("🔔 Reminder: Check server logs", "reminder")
    ]
    
    print(f"Adding {len(test_messages)} messages to queue...")
    
    success_count = 0
    for i, (message_text, message_type) in enumerate(test_messages, 1):
        message = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.datetime.now().isoformat(),
            "message_body": {
                "message_text": message_text,
                "sent": False,
                "message_type": message_type
            }
        }
        
        try:
            result = queue.add_message(message)
            if result:
                print(f"✅ {i}. Added: {message_text}")
                success_count += 1
            else:
                print(f"❌ {i}. Failed: {message_text}")
        except Exception as e:
            print(f"❌ {i}. Error: {e}")
    
    print(f"\n📊 Results: {success_count}/{len(test_messages)} messages added successfully")
    
    # Verify total messages in queue
    try:
        messages = queue.get_messages()
        print(f"📋 Total messages in queue: {len(messages)}")
    except Exception as e:
        print(f"❌ Could not retrieve queue status: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "multiple":
        test_add_multiple_messages()
    else:
        test_add_message()
