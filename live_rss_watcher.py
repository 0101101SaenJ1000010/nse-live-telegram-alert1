import requests
import xml.etree.ElementTree as ET
import time
from datetime import datetime

# RSS Feed URL
FEED_URL = "https://nsearchives.nseindia.com/content/RSS/Financial_Results.xml"
FEED_NAME = "FinResult"

# Telegram Bot Config
BOT_TOKEN = '8165623622:AAGIPRrU5rdX4EmNUFT_IDvHDGjuMpWQAI0'
CHAT_ID = '5501599635'

# Track sent announcements
seen_links = set()

# HTTP Headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Send message to Telegram
def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        print(f"[Telegram Error] {e}")

# Fetch RSS data
def fetch_rss_feed():
    try:
        response = requests.get(FEED_URL, headers=headers, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"[Fetch Error] {e}")
        return None

# Extract PDF link
def extract_attachment_link(description):
    if ".pdf" in description:
        start = description.find("https://")
        end = description.find(".pdf") + 4
        return description[start:end]
    return "N/A"

# Parse and process feed
def parse_and_display(xml):
    root = ET.fromstring(xml)
    items = root.findall(".//item")

    for item in items:
        title = item.findtext("title", default="N/A").strip()
        link = item.findtext("link", default="N/A").strip()
        description = item.findtext("description", default="").strip()

        if link in seen_links:
            continue
        seen_links.add(link)

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        attachment = extract_attachment_link(description)

        print("=" * 70)
        print(f"🕒 Announcement at : {now} IST")
        print(f"🏢 Stock name      : {title}")
        print(f"📝 Description     :\n{description}")
        print(f"🔗 Update link     : {link}")
        print(f"📎 Attachment link : {attachment}")
        print(f"🧾 NSE Feed        : {FEED_NAME}")
        print(f"📘 Other Info      : _\n")

        # Send to Telegram
        message = (
            f"<b>{FEED_NAME} Alert</b>\n"
            f"🕒 <b>Time</b>: {now} IST\n"
            f"🏢 <b>Stock</b>: {title}\n"
            f"📝 <b>Description</b>: {description or 'N/A'}\n"
            f"🔗 <b>Link</b>: {link}\n"
            f"📎 <b>Attachment</b>: {attachment}"
        )
        send_telegram_message(message)

# Main Watcher
def watch():
    print("📡 Monitoring NSE Online Announcements...\n")
    while True:
        xml = fetch_rss_feed()
        if xml:
            parse_and_display(xml)
        time.sleep(120)  # every 2 minutes

if __name__ == "__main__":
    watch()
