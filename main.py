import re
import requests
import feedparser

TELEGRAM_TOKEN = "8612771945:AAHbD44K221emkUajjd23IMzzZ8by4KJwa8"
CHAT_ID = "7363628781"

RSS_FEEDS = [
    "https://www.globenewswire.com/rss/feed/inline",
    "https://www.prnewswire.com/rss/news-releases-list.rss",
    "https://feed.businesswire.com/rss/home/?rss=G1QFDFRHSEF3"
]

BLACK_LIST = r"Class Action|Shareholder Alert|Brodsky & Smith|Kaplan Fox|Frank R. Cruz|Investigation|Dividend|Conference|to Present|Earnings Report|Filing of Notice|Notice of Pendency|Reminds Investors|Lead Plaintiff"
WHITE_LIST = r"FDA Approval|FDA|Phase 3|Phase 2|Clinical Trial|Breakthrough Therapy|Orphan Drug|Fast Track|Acquisition|Buyout|Merger|Definitive Agreement|Strategic Partnership|Joint Venture|Multi-Million Dollar Contract|Contract Award|Patent Issued|ARPA-H Funding|BARDA|NIH Grant|Exclusive License|Commercialization"

def check_stock_radar():
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                link = getattr(entry, 'link', '')
                title = getattr(entry, 'title', '')

                if re.search(BLACK_LIST, title, re.IGNORECASE):
                    continue

                if not re.search(WHITE_LIST, title, re.IGNORECASE):
                    continue

                match = re.search(r'\(([A-Z]+)\)', title)
                if not match:
                    continue
                symbol = match.group(1)

                try:
                    yf_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                    res = requests.get(yf_url, headers=headers, timeout=5).json()
                    
                    meta = res['chart']['result'][0]['meta']
                    price = meta.get('regularMarketPrice', 0)
                    exchange = meta.get('exchangeName', '')

                    if 1 <= price <= 10 and exchange in ['NASDAQ', 'NYSE', 'AMEX']:
                        msg = (
                            f"🚀 **DEV PATLAMA ADAYI SİNYALİ!**\n\n"
                            f"📌 **Kod:** `{symbol}`\n"
                            f"💰 **Fiyat:** `${price}`\n"
                            f"🏛 **Borsa:** {exchange}\n\n"
                            f"📰 **Haber:** {title}\n\n"
                            f"🔗 [Habere Git]({link})\n"
                            f"🔍 [Zoya İslami Finans Kontrolü](https://zoya.finance/stocks/{symbol})"
                        )
                        
                        requests.post(
                            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                            json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
                        )
                except Exception:
                    continue
        except Exception:
            continue

if __name__ == "__main__":
    check_stock_radar()
  
