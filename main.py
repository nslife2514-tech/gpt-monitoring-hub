import os
import requests
import feedparser

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

RSS_URL = "https://news.google.com/rss/search?q=ราชกิจจานุเบกษา&hl=th&gl=TH&ceid=TH:th"

KEYWORDS = [
    "โรงงาน",
    "อุตสาหกรรม",
    "อาคาร",
    "ควบคุมอาคาร",
    "ดับเพลิง",
    "อัคคีภัย",
    "ความปลอดภัย",
    "แรงงาน",
    "สิ่งแวดล้อม",
    "พลังงาน",
    "ก๊าซ",
    "วัตถุอันตราย",
    "สารเคมี"
]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

feed = feedparser.parse(RSS_URL)

found = False

for entry in feed.entries[:10]:
    title = entry.title
    link = entry.link
    text_to_check = title

    matched_keywords = [kw for kw in KEYWORDS if kw in text_to_check]

    if matched_keywords:
        message = f"""
⚠ GPT Monitoring Hub

พบข้อมูลที่อาจเกี่ยวข้องกับงานวิศวกรรม / โรงงาน / ความปลอดภัย

หัวข้อ:
{title}

Keyword ที่พบ:
{", ".join(matched_keywords)}

สถานะ:
ℹ Search Layer Alert
ยังไม่ได้ยืนยัน PDF ราชกิจจาฯ

Link:
{link}
"""
        send_telegram(message)
        found = True

if not found:
    print("No relevant alert found.")
else:
    print("Relevant alert sent.")
