import requests
import time
import xml.etree.ElementTree as ET

BOT_TOKEN = '8165623622:AAGIPRrU5rdX4EmNUFT_IDvHDGjuMpWQAI0'
CHAT_ID = '5501599635'

# List of NSE RSS URLs
rss_urls = [
    "https://nsearchives.nseindia.com/content/equities/eqDividend.xml",
    "https://nsearchives.nseindia.com/content/RSS/Corporate_action.xml"
]

sent_titles = set()

def fetch_rss(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_and_send(xml_data):
    root = ET.fromstring(xml_data)
    for item in root.findall(".//item"):
        title = item.find("title").text.strip() if item.find("title") is not None else "No Title"
        if title not in sent_titles:
            message = f"📢 *Announcement Title:* {title}"
            send_telegram(message)
            print(f"✅ Sent: {title}")
            sent_titles.add(title)

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print(f"❌ Telegram error: {e}")

# Loop forever every 5 minutes
while True:
    for rss_url in rss_urls:
        xml_data = fetch_rss(rss_url)
        if xml_data:
            parse_and_send(xml_data)
    time.sleep(300)  # Sleep for 5 minutes
