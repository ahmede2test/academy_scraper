import os
import feedparser
import re
import random
from supabase import create_client

# إعدادات الربط
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(URL, KEY)

def get_joker_image():
    """قائمة الصور الاحترافية الثابتة - اخترنا لك أفضل الصور البرمجية"""
    pro_images = [
        "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&q=80",
        "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800&q=80",
        "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=800&q=80",
        "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800&q=80",
        "https://images.unsplash.com/photo-1587620962725-abab7fe55159?w=800&q=80",
        "https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=800&q=80",
        "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&q=80",
        "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&q=80",
        "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&q=80",
        "https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=800&q=80"
    ]
    # اختيار صورة عشوائية من القائمة لضمان عدم التكرار الممل
    return random.choice(pro_images)

def start_scraping():
    # المصادر التقنية
    sources = [
        {"url": "https://aitnews.com/category/برمجيات-وعلوم-حاسب/feed/", "cat": "برمجيات"},
        {"url": "https://www.tech-wd.com/wd/category/programming/feed/", "cat": "برمجة"},
        {"url": "https://arabhardware.net/news/feed", "cat": "أخبار التقنية"}
    ]
    
    print("🚀 جاري سحب الأخبار بنظام الجوكر للصور...")
    
    for source in sources:
        feed = feedparser.parse(source['url'])
        author_name = feed.feed.title.split('-')[0].strip() if 'title' in feed.feed else "مصدر تقني"
        
        for entry in feed.entries[:12]:
            # استخدام نظام الجوكر للصور لضمان الجودة
            img_url = get_joker_image()

            # تنظيف المحتوى من وسوم HTML
            content_raw = entry.summary if 'summary' in entry else entry.title
            content_clean = re.sub(r'<[^>]+>', '', content_raw).strip()
            if len(content_clean) > 250:
                content_clean = content_clean[:247] + "..."

            news_data = {
                "title": entry.title,
                "image_url": img_url,
                "content": content_clean,
                "author": author_name,
                "category": source['cat']
            }
            
            try:
                # الرفع لـ Supabase
                supabase.table("academy_news").upsert(news_data, on_conflict='title').execute()
            except Exception as e:
                print(f"❌ خطأ في خبر: {entry.title[:20]}..")
                continue
                
    print("✅ تم التحديث! الصور الآن مستقرة 100% وتظهر للجميع.")

if __name__ == "__main__":
    start_scraping()
