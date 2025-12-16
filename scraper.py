import os
import feedparser
from supabase import create_client

# ربط المفاتيح من الخزنة
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(URL, KEY)

def start_scraping():
    # روابط الأخبار (RSS) - دي أسرع وسيلة تجيب أخبار كتير
    sources = [
        "https://aitnews.com/feed/",
        "https://www.tech-wd.com/wd/feed/",
        "https://www.unlimit-tech.com/feed/"
    ]
    
    print("📡 جاري جمع الأخبار...")
    for url in sources:
        feed = feedparser.parse(url)
        for entry in feed.entries[:20]:  # هيسحب 20 خبر من كل موقع
            news_data = {
                "title": entry.title,
                "image_url": "https://img.freepik.com/free-vector/breaking-news-concept_23-2148514216.jpg",
                "content": f"لقراءة التفاصيل: {entry.link}"
            }
            # إضافة الخبر (ولو موجود قبل كدة هيعمل له تحديث مش تكرار)
            try:
                supabase.table("academy_news").upsert(news_data, on_conflict='title').execute()
            except:
                continue
    print("✅ خلصت! روح شوف الجدول دلوقتي.")

if __name__ == "__main__":
    start_scraping()
