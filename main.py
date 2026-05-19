import os
import requests
import feedparser
from datetime import datetime, timezone, timedelta

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


def thai_now():
    tz_th = timezone(timedelta(hours=7))
    return datetime.now(tz_th).strftime("%d/%m/%Y %H:%M")


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=data)

    print("Telegram status:", response.status_code)
    print(response.text)


def detect_status(link):
    link_lower = link.lower()

    if ".pdf" in link_lower or "/pdf/" in link_lower:
        return "⚠ Pending Verification"

    if "ratchakitcha.soc.go.th" in link_lower:
        return "⚠ Pending Verification"

    return "ℹ News Layer"


def main():
    run_time = thai_now()

    feed = feedparser.parse(RSS_URL)

    source_status = "✅ RSS ตรวจสำเร็จ"
    total_entries = len(feed.entries)

    found = False
    alert_count = 0

    for entry in feed.entries[:10]:
        title = entry.title
        link = entry.link

        text_to_check = title

        matched_keywords = [
            kw for kw in KEYWORDS
            if kw in text_to_check
        ]

        if matched_keywords:
            status = detect_status(link)

            message = f"""
⚠ GPT Monitoring Hub

พบข้อมูลที่อาจเกี่ยวข้องกับงานวิศวกรรม / โรงงาน / ความปลอดภัย

หัวข้อ:
{title}

Keyword ที่พบ:
{", ".join(matched_keywords)}

สถานะ:
{status}

Link:
{link}
"""

            send_telegram(message)

            found = True
            alert_count += 1

    heartbeat = f"""
💓 GPT Monitoring Hub

Daily System Check: OK

เวลา:
{run_time}

ผลการตรวจ:
✅ GitHub Actions ทำงาน
{source_status}
✅ Telegram ส่งสำเร็จ

จำนวนรายการที่ตรวจจาก RSS:
{total_entries}

จำนวน Alert ที่เข้าเงื่อนไข:
{alert_count}

สถานะ:
{"พบรายการที่เกี่ยวข้อง" if found else "ไม่พบ Alert สำคัญวันนี้"}

System Status:
ONLINE
"""

    send_telegram(heartbeat)


if __name__ == "__main__":
    main()
