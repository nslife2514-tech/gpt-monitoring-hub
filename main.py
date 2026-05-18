import requests

BOT_TOKEN = "8801312116:AAGWFN1wj5EDglZQ3DsYE0IhzhHQRkSabOg"
CHAT_ID = "8750288749"

message = "🚀 GPT Monitoring Hub Started Successfully"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": message
}

requests.post(url, data=data)

print("Message sent!")
