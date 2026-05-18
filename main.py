import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ทดลองจำลองการพบประกาศใหม่
title = "พบประกาศใหม่ในราชกิจจานุเบกษา"
source = "https://ratchakitcha.soc.go.th/"

message = f"""
⚠ GPT Monitoring Hub

{title}

Source:
{source}
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": message
}

requests.post(url, data=data)

print("Alert sent!")
