import os
import feedparser
import re
import random
from supabase import create_client

# 1. إعدادات الربط - سحب القيم من GitHub Secrets
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(URL, KEY)

# --- [قسم الأخبار: 50 صورة احترافية] ---

def get_50_tech_images():
    """قائمة بـ 50 صورة تقنية عالية الجودة لضمان التنوع"""
    base_images = [
        "https://images.unsplash.com/photo-1518770660439-4636190af475",
        "https://images.unsplash.com/photo-1461749280684-dccba630e2f6",
        "https://images.unsplash.com/photo-1498050108023-c5249f4df085",
        "https://images.unsplash.com/photo-1504639725590-34d0984388bd",
        "https://images.unsplash.com/photo-1587620962725-abab7fe55159",
        "https://images.unsplash.com/photo-1517694712202-14dd9538aa97",
        "https://images.unsplash.com/photo-1555066931-4365d14bab8c",
        "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5",
        "https://images.unsplash.com/photo-1534667762233-3b567d6ea065",
        "https://images.unsplash.com/photo-1550751827-4bd374c3f58b",
        "https://images.unsplash.com/photo-1510915228340-29c85a43dcfe",
        "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2",
        "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b",
        "https://images.unsplash.com/photo-1515879218367-8466d910aaa4",
        "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158",
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f",
        "https://images.unsplash.com/photo-1531297484001-80022131f5a1",
        "https://images.unsplash.com/photo-1542744094-3a31f272c490",
        "https://images.unsplash.com/photo-1571171637578-41bc2dd41cd2",
        "https://images.unsplash.com/photo-1504384308090-c894fdcc538d",
        "https://images.unsplash.com/photo-1514030849962-49da450429b6",
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa",
        "https://images.unsplash.com/photo-1516116216624-53e697fedbea",
        "https://images.unsplash.com/photo-1551434678-e076c223a692",
        "https://images.unsplash.com/photo-1519389950473-47ba0277781c",
        "https://images.unsplash.com/photo-1496171367470-9ed9a91ea931",
        "https://images.unsplash.com/photo-1537432376769-00f5c2f4c8d2",
        "https://images.unsplash.com/photo-1503437313881-503a91226402",
        "https://images.unsplash.com/photo-1550439062-609e1531270e",
        "https://images.unsplash.com/photo-1580894732444-8ecdead79730",
        "https://images.unsplash.com/photo-1551033406-611cf9a28f67",
        "https://images.unsplash.com/photo-1484417894907-623942c8ee29",
        "https://images.unsplash.com/photo-1562813733-b31f71025d54",
        "https://images.unsplash.com/photo-1536104968055-4d61aa56f46a",
        "https://images.unsplash.com/photo-1523961131990-5ea7c61b2107",
        "https://images.unsplash.com/photo-1558494949-ef010cbdcc51",
        "https://images.unsplash.com/photo-1517139274687-b927132cd2f7",
        "https://images.unsplash.com/photo-1516259762381-22954d7d3ad2",
        "https://images.unsplash.com/photo-1508921234172-b68ed335b3e6",
        "https://images.unsplash.com/photo-1520085601670-ee14aa58e822",
        "https://images.unsplash.com/photo-1551288049-bbbda50a26a1",
        "https://images.unsplash.com/photo-1518433278985-1628127953a1",
        "https://images.unsplash.com/photo-1544197150-b99a580bb7a8",
        "https://images.unsplash.com/photo-1523966211575-eb4a01e7dd51",
        "https://images.unsplash.com/photo-1454165833267-0352c6f3796d",
        "https://images.unsplash.com/photo-1509062522246-37559ee23c75",
        "https://images.unsplash.com/photo-1519241047957-be31d7379a5d",
        "https://images.unsplash.com/photo-1485827404703-89b55fcc595e",
        "https://images.unsplash.com/photo-1535223289827-42f1e9919769",
        "https://images.unsplash.com/photo-1504384764586-bb4cdc17457f"
    ]
    # تهيئة الروابط مع بارامترات الجودة
    return [f"{url}?w=800&q=80&auto=format&fit=crop" for url in base_images]

def start_news_scraping():
    print("🚀 بدء سحب الأخبار بـ 50 صورة متنوعة...")
    sources = [
        {"url": "https://aitnews.com/category/برمجيات-وعلوم-حاسب/feed/", "cat": "برمجيات"},
        {"url": "https://www.tech-wd.com/wd/category/programming/feed/", "cat": "برمجة"}
    ]
    img_pool = get_50_tech_images()
    
    for source in sources:
        feed = feedparser.parse(source['url'])
        for entry in feed.entries[:10]:
            news_data = {
                "title": entry.title,
                "image_url": random.choice(img_pool),
                "content": re.sub(r'<[^>]+>', '', entry.summary[:300]) if 'summary' in entry else entry.title,
                "author": "مصدر تقني",
                "category": source['cat']
            }
            try:
                supabase.table("academy_news").upsert(news_data, on_conflict='title').execute()
            except Exception as e:
                print(f"⚠️ فشل رفع خبر: {e}")
    print("✅ تم تحديث الأخبار بالصور الـ 50 بنجاح.")

# --- [قسم الدروس: سحب RSS المستقر بدون API Key] ---

def sync_lessons_by_rss():
    print("🔄 بدء سحب الدروس عبر تقنية RSS (طريقة مستقرة)...")
    channels = [
        {"id": "UC8butISFwT-Wl7EV0hUK0BQ", "course_id": 1, "name": "FreeCodeCamp (CS50)"},
        {"id": "UCW5YeuERMmlnqo4ra8qBxNA", "course_id": 2, "name": "The Net Ninja (Flutter)"},
        {"id": "UC29ju8bIPH5as8OGnQzwJyA", "course_id": 3, "name": "Traversy Media (Python)"}
    ]

    for channel in channels:
        try:
            rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel['id']}"
            feed = feedparser.parse(rss_url)
            
            # التأكد من وجود الكورس أولاً
            supabase.table("courses").upsert({"id": channel['course_id'], "title": channel['name']}).execute()
            
            lessons = []
            for index, entry in enumerate(feed.entries[:15]): # سحب آخر 15 فيديو
                video_id = entry.link.split("v=")[1]
                lessons.append({
                    "course_id": channel['course_id'],
                    "title": entry.title,
                    "video_url": f"https://www.youtube.com/watch?v={video_id}",
                    "order_index": index + 1
                })
            
            if lessons:
                supabase.table("lessons").upsert(lessons, on_conflict='video_url').execute()
                print(f"✅ نجاح: تم رفع {len(lessons)} درس من {channel['name']}")
                
        except Exception as e:
            print(f"❌ خطأ في قناة {channel['name']}: {e}")

# --- [التشغيل الرئيسي] ---

if __name__ == "__main__":
    start_news_scraping()    # تحديث الأخبار بالصور الـ 50
    sync_lessons_by_rss()   # تحديث الدروس بدون مشاكل API
    print("🏁 اكتملت جميع العمليات بنجاح!")
