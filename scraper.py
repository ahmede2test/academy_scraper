import os
import feedparser
import re
import urllib.parse
from supabase import create_client

# إعدادات الربط
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(URL, KEY)

def get_unique_tech_image(title):
    """جلب صورة مميزة وعالية الجودة بناءً على كلمات من العنوان"""
    # تنظيف العنوان من الرموز وترجمة بعض الكلمات للإنجليزية لتحسين البحث
    clean_title = re.sub(r'[^\w\s]', '', title)
    # كلمات دلالية تجعل الصور دائماً برمجية وتقنية
    tech_keywords = "programming,coding,technology,software"
    # تحويل العنوان إلى صيغة URL
    encoded_query = urllib.parse.quote(f"{tech_keywords},{clean_title}")
    # استخدام sig لجعل Unsplash يولد صورة فريدة لكل خبر بناءً على طول العنوان
    return f"https://images.unsplash.com/featured/?{encoded_query}&sig={len(title) + hash(title)}"

def start_scraping():
    sources = [
        {"url": "https://aitnews.com/category/برمجيات-وعلوم-حاسب/feed/", "cat": "برمجيات"},
        {"url": "https://www.tech-wd.com/wd/category/programming/feed/", "cat": "برمجة"},
        {"url": "https://www.unlimit-tech.com/category/programming/feed/", "cat": "تطوير"}
    ]
    
    print("🚀 جاري سحب أخبار البرمجة بصور مميزة...")
    
    for source in sources:
        feed = feedparser.parse(source['url'])
        # استخراج اسم الموقع
        author_name = feed.feed.title.split('-')[0].strip() if 'title' in feed.feed else "مصدر تقني"
        
        for entry in feed.entries[:15]:
            # 1. جلب صورة مميزة وفريدة لكل خبر بناءً على عنوانه
            img_url = get_unique_tech_image(entry.title)

            # 2. تنظيف المحتوى
            content_raw = entry.summary if 'summary' in entry else entry.title
            content_clean = re.sub(r'<[^>]+>', '', content_raw).strip()

            news_data = {
                "title": entry.title,
                "image_url": img_url,
                "content": content_clean,
                "author": author_name,
                "category": source['cat']
            }
            
            try:
                # تحديث الخبر أو إضافته
                supabase.table("academy_news").upsert(news_data, on_conflict='title').execute()
            except Exception as e:
                continue
                
    print("✅ تم التحديث! الصور الآن ستكون مميزة ومختلفة لكل خبر.")

if __name__ == "__main__":
    start_scraping()
