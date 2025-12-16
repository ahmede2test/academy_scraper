import os
import feedparser
from supabase import create_client

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(URL, KEY)

def start_scraping():
    # مصادر متنوعة لضمان محتوى متجدد وصور مختلفة
    sources = [
        "https://aitnews.com/feed/",
        "https://www.tech-wd.com/wd/feed/",
        "https://www.unlimit-tech.com/feed/"
    ]
    
    for url in sources:
        feed = feedparser.parse(url)
        for entry in feed.entries[:15]:
            # 1. محاولة استخراج الصورة الحقيقية من المرفقات
            image_url = "https://via.placeholder.com/600x400" # افتراضي في حال فشل كل المحاولات
            if 'media_content' in entry:
                image_url = entry.media_content[0]['url']
            elif 'links' in entry:
                for link in entry.links:
                    if 'image' in link.get('type', ''):
                        image_url = link.href
            
            # 2. تنظيف المحتوى (سحب الوصف وليس الرابط)
            content = entry.summary if 'summary' in entry else entry.title

            news_data = {
                "title": entry.title,
                "image_url": image_url,
                "content": content
            }
            try:
                # تحديث لو موجود أو إضافة لو جديد بناءً على العنوان
                supabase.table("academy_news").upsert(news_data, on_conflict='title').execute()
            except:
                continue

if __name__ == "__main__":
    start_scraping()
