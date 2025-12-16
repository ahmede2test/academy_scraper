import os
import feedparser
from supabase import create_client

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(URL, KEY)

def start_scraping():
    # مصادر أخبار تقنية تدعم الـ RSS بشكل ممتاز
    sources = [
        "https://aitnews.com/feed/",
        "https://www.tech-wd.com/wd/feed/",
        "https://www.unlimit-tech.com/feed/"
    ]
    
    for url in sources:
        feed = feedparser.parse(url)
        for entry in feed.entries[:20]:
            # 1. سحب وصف الخبر بدلاً من الرابط
            description = entry.summary if 'summary' in entry else entry.title
            
            # 2. محاولة سحب صورة الخبر الأصلية
            image_url = "https://via.placeholder.com/600x400"
            if 'media_content' in entry:
                image_url = entry.media_content[0]['url']
            elif 'links' in entry:
                for link in entry.links:
                    if 'image' in link.get('type', ''):
                        image_url = link.href

            news_data = {
                "title": entry.title,
                "image_url": image_url,
                "content": description # هنا سحبنا الوصف وليس اللينك
            }
            try:
                supabase.table("academy_news").upsert(news_data, on_conflict='title').execute()
            except:
                continue

if __name__ == "__main__":
    start_scraping()
