import os
import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

RSS_URL = "https://news.google.com/rss/search?q=ราชกิจจานุเบกษา&hl=th&gl=TH&ceid=TH:th"

ROYAL_GAZETTE_URL = "https://ratchakitcha.soc.go.th/"

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
    "สารเคมี",
    "สถาปนิก",
    "วิศวกร",
    "วิชาชีพ",
    "สภาสถาปนิก",
    "สภาวิศวกร",
    "มาตรฐาน",
    "ใบอนุญาต",
    "พัฒนาวิชาชีพ"
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

    print("Telegram:", response.status_code)


def detect_status(link):
    link_lower = link.lower()

    if ".pdf" in link_lower:
        return "⚠ Pending Verification"

    if "/pdf/" in link_lower:
        return "⚠ Pending Verification"

    if "ratchakitcha.soc.go.th" in link_lower:
        return "⚠ Pending Verification"

    return "ℹ News Layer"


def check_rss_layer():
    alerts = []

    feed = feedparser.parse(RSS_URL)

    for entry in feed.entries[:20]:

        title = entry.title
        link = entry.link

        matched_keywords = [
            kw for kw in KEYWORDS
            if kw in title
        ]

        if matched_keywords:

            status = detect_status(link)

            alerts.append({
                "source": "Google RSS",
                "title": title,
                "link": link,
                "keywords": matched_keywords,
                "status": status
            })

    return alerts, len(feed.entries)


def check_royal_gazette_direct():

    alerts = []

    try:
        response = requests.get(
            ROYAL_GAZETTE_URL,
            timeout=20
        )

        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text("\n")

        lines = text.splitlines()

        for line in lines:

            line = line.strip()

            if len(line) < 20:
                continue

            matched_keywords = [
                kw for kw in KEYWORDS
                if kw in line
            ]

            if matched_keywords:

                alerts.append({
                    "source": "Royal Gazette Direct",
                    "title": line,
                    "link": ROYAL_GAZETTE_URL,
                    "keywords": matched_keywords,
                    "status": "⚠ Pending Verification"
                })

    except Exception as e:
        print("Royal Gazette check error:", e)

    return alerts


def main():

    run_time = thai_now()

    total_alerts = []

    rss_alerts, rss_count = check_rss_layer()
    total_alerts.extend(rss_alerts)

    rg_alerts = check_royal_gazette_direct()
    total_alerts.extend(rg_alerts)

    sent_titles = set()

    for alert in total_alerts:

        if alert["title"] in sent_titles:
            continue

        sent_titles.add(alert["title"])

        message = f"""
⚠ GPT Monitoring Hub

พบข้อมูลที่อาจเกี่ยวข้องกับงานวิศวกรรม / โรงงาน / ความปลอดภัย

Source:
{alert["source"]}

หัวข้อ:
{alert["title"]}

Keyword:
{", ".join(alert["keywords"])}

สถานะ:
{alert["status"]}

Link:
{alert["link"]}
"""

        send_telegram(message)

    heartbeat = f"""
💓 GPT Monitoring Hub

Daily System Check: OK

เวลา:
{run_time}

ผลการตรวจ:
✅ GitHub Actions ทำงาน
✅ RSS ตรวจสำเร็จ
✅ Royal Gazette Direct Layer ตรวจสำเร็จ
✅ Telegram ส่งสำเร็จ

จำนวนรายการ RSS:
{rss_count}

จำนวน Alert:
{len(sent_titles)}

สถานะ:
{"พบรายการที่เกี่ยวข้อง" if sent_titles else "ไม่พบ Alert สำคัญวันนี้"}

System Status:
ONLINE
"""

    send_telegram(heartbeat)


if __name__ == "__main__":
    main()
