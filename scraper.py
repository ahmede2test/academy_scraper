import os
import feedparser
import re
from supabase import create_client

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(URL, KEY)

def start_scraping():
    # مصادر متخصصة في البرمجة وعلوم الحاسب
    sources = [
        {"url": "https://aitnews.com/category/برمجيات-وعلوم-حاسب/feed/", "cat": "برمجيات"},
        {"url": "https://www.tech-wd.com/wd/category/programming/feed/", "cat": "برمجة"},
        {"url": "https://www.unlimit-tech.com/category/programming/feed/", "cat": "تطوير"}
    ]
    
    for source in sources:
        feed = feedparser.parse(source['url'])
        author_name = feed.feed.title if 'title' in feed.feed else "مصدر تقني"
        
        for entry in feed.entries[:15]:
            # استخراج الصورة الحقيقية
            img_url = "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=1000" # صورة برمجية افتراضية
            if 'media_content' in entry:
                img_url = entry.media_content[0]['url']
            elif 'description' in entry:
                match = re.search(r'<img[^>]+src="([^">]+)"', entry.description)
                if match: img_url = match.group(1)

            # تنظيف المحتوى من روابط التحويل
            content_clean = entry.summary if 'summary' in entry else entry.title
            content_clean = re.sub(r'<[^>]+>', '', content_clean) # مسح أي كود HTML

            news_data = {
                "title": entry.title,
                "image_url": img_url,
                "content": content_clean,
                "author": author_name,
                "category": source['cat']
            }
            
            try:
                supabase.table("academy_news").upsert(news_data, on_conflict='title').execute()
            except:
                continue
    print("✅ تم تحديث أخبار البرمجة بنجاح!")

if __name__ == "__main__":
    start_scraping()
