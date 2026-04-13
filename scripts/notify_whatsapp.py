import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

PHONE = os.getenv("CALLMEBOT_PHONE")
API_KEY = os.getenv("CALLMEBOT_APIKEY")
CALLMEBOT_URL = "https://api.callmebot.com/whatsapp.php"


def send_whatsapp(message: str):
    if not PHONE or not API_KEY:
        raise ValueError("CALLMEBOT_PHONE or CALLMEBOT_APIKEY is not set")
    encoded = quote(message)
    url = f"{CALLMEBOT_URL}?phone={PHONE}&text={encoded}&apikey={API_KEY}"
    print(f"[notify] Calling CallMeBot API for {PHONE}")
    resp = requests.get(url, timeout=15)
    if resp.status_code == 200:
        print("WhatsApp message sent successfully.")
    else:
        raise RuntimeError(f"CallMeBot API error: HTTP {resp.status_code} — {resp.text[:300]}")
