import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

PHONE = os.getenv("CALLMEBOT_PHONE")
API_KEY = os.getenv("CALLMEBOT_APIKEY")
CALLMEBOT_URL = "https://api.callmebot.com/whatsapp.php"


def send_whatsapp(message: str):
    encoded = quote(message)
    url = f"{CALLMEBOT_URL}?phone={PHONE}&text={encoded}&apikey={API_KEY}"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            print("WhatsApp message sent successfully.")
        else:
            print(f"Failed to send WhatsApp message: HTTP {resp.status_code} — {resp.text[:200]}")
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")
