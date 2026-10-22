import os
import feedparser
import requests

# Güvenli token ve senin doğru Chat ID'n
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = "7363628781"

RSS_FEEDS = [
    "https://www.globenewswire.com/rss/feed/inline"
]

def test_telegram_radar():
    if not TELEGRAM_TOKEN:
        print("Hata: TELEGRAM_BOT_TOKEN bulunamadı!")
        return

    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            if feed.entries:
                # Test amaçlı akıştaki ilk haberi alıyoruz (hiçbir filtre yok)
                entry = feed.entries[0]
                link = getattr(entry, 'link', '')
                title = getattr(entry, 'title', '')

                msg = (
                    f"🧪 **TEST MESAJI (Filtresiz Çalışıyor!)**\n\n"
                    f"📰 **Haber Başlığı:** {title}\n\n"
                    f"🔗 [Habere Git]({link})"
                )

                response = requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
                )
                print(f"Telegram Yanıt Durumu: {response.status_code}")
                break # Sadece bir test mesajı atıp döngüyü bitiriyoruz
        except Exception as e:
            print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    test_telegram_radar()
