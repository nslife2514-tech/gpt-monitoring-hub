import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

message = "✅ GPT Monitoring Hub: Secret setup completed"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": message
}

requests.post(url, data=data)

print("Message sent!")
