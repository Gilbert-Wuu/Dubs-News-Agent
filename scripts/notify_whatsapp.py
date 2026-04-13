import os
import requests
from dotenv import load_dotenv

load_dotenv()

PHONE = os.getenv("CALLMEBOT_PHONE")
API_KEY = os.getenv("CALLMEBOT_APIKEY")
CALLMEBOT_URL = "https://api.callmebot.com/whatsapp.php"


def send_whatsapp(message: str):
    if not PHONE or not API_KEY:
        raise ValueError("CALLMEBOT_PHONE or CALLMEBOT_APIKEY is not set")
    print(f"[notify] Calling CallMeBot API for {PHONE}")
    resp = requests.get(CALLMEBOT_URL, params={
        "phone": PHONE,
        "text": message,
        "apikey": API_KEY,
    }, timeout=15)
    print(f"CallMeBot response ({resp.status_code}): {resp.text[:300]}")
    if resp.status_code != 200:
        raise RuntimeError(f"CallMeBot API error: HTTP {resp.status_code}")
