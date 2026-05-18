import os
import requests
import feedparser

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

RSS_URL = "https://news.google.com/rss/search?q=ราชกิจจานุเบกษา&hl=th&gl=TH&ceid=TH:th"

feed = feedparser.parse(RSS_URL)

if feed.entries:
    latest = feed.entries[0]

    title = latest.title
    link = latest.link

    message = f"""
⚠ GPT Monitoring Hub

พบข้อมูลใหม่เกี่ยวกับราชกิจจานุเบกษา

หัวข้อ:
{title}

Link:
{link}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)

    print("Alert sent!")

else:
    print("No news found.")
