import os
import feedparser
import requests

print("--- BOT ÇALIŞMAYA BAŞLADI ---")

# Token kontrolü
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = "7363628781"

if not TELEGRAM_TOKEN:
    print("HATA: TELEGRAM_BOT_TOKEN bulunamadı! GitHub Secrets ayarlarını kontrol et.")
    exit(1)
else:
    print("TOKEN: Başarıyla alındı.")

# Güvenilir bir RSS kaynağı
url = "https://www.globenewswire.com/rss/feed/inline"
print(f"RSS adresi taranıyor: {url}")

feed = feedparser.parse(url)

if not feed.entries:
    print("HATA: RSS kaynağından hiç haber çekilemedi!")
    exit(1)

# Akıştaki ilk haberi alıyoruz
entry = feed.entries[0]
title = getattr(entry, 'title', 'Başlık Yok')
link = getattr(entry, 'link', 'Link Yok')

print(f"Bulunan Haber Başlığı: {title}")

# Telegram mesajı hazırlama
msg = f"🧪 **TEST MESAJI (Direkt Çekildi)**\n\n📰 {title}\n\n🔗 {link}"

telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": msg,
    "parse_mode": "Markdown"
}

print("Telegram'a mesaj gönderiliyor...")
response = requests.post(telegram_url, json=payload)

print(f"Telegram Yanıt Kodu: {response.status_code}")
print(f"Telegram Yanıt İçeriği: {response.text}")

if response.status_code == 200:
    print("BAŞARILI: Mesaj Telegram'a iletildi!")
else:
    print("HATA: Telegram mesajı reddetti!")
