import os
import feedparser
import re
import random
from supabase import create_client
from googleapiclient.discovery import build

# 1. إعدادات الربط - تأكد من صحة المسميات في GitHub Secrets
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")  # يفضل استخدام service_role key هنا
YT_KEY = os.getenv("YOUTUBE_API_KEY")

# تهيئة العملاء
try:
    supabase = create_client(URL, KEY)
    youtube = build('youtube', 'v3', developerKey=YT_KEY)
except Exception as e:
    print(f"❌ خطأ في التهيئة الأولية: {e}")

def get_fixed_images():
    images = [
        "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800",
        "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800",
        "https://images.unsplash.com/photo-1587620962725-abab7fe55159?w=800"
    ]
    random.shuffle(images)
    return images

def start_news_scraping():
    print("🚀 بدء سحب الأخبار...")
    sources = [
        {"url": "https://aitnews.com/category/برمجيات-وعلوم-حاسب/feed/", "cat": "برمجيات"},
        {"url": "https://www.tech-wd.com/wd/category/programming/feed/", "cat": "برمجة"}
    ]
    img_pool = get_fixed_images()
    
    for source in sources:
        feed = feedparser.parse(source['url'])
        for entry in feed.entries[:5]:
            news_data = {
                "title": entry.title,
                "image_url": random.choice(img_pool),
                "content": entry.summary[:250] if 'summary' in entry else entry.title,
                "author": "مصدر تقني",
                "category": source['cat']
            }
            try:
                supabase.table("academy_news").upsert(news_data, on_conflict='title').execute()
            except Exception as e:
                print(f"⚠️ فشل رفع خبر: {e}")
    print("✅ اكتمل تحديث الأخبار.")

def sync_lessons():
    print("🔄 جاري تحديث الكورسات والدروس...")
    
    # ضمان وجود الكورسات أولاً لتجنب خطأ Foreign Key
    courses_data = [
        {"id": 1, "title": "CS50 - علوم الحاسب"},
        {"id": 2, "title": "Flutter - تطبيقات"},
        {"id": 3, "title": "Python - لغة بايثون"}
    ]
    try:
        supabase.table("courses").upsert(courses_data).execute()
    except Exception as e:
        print(f"⚠️ تنبيه: لم يتم تحديث جدول الكورسات، قد يكون RLS مفعلاً: {e}")

    playlists = [
        ("PLDoPjvoNmBAw6p0z0Ek0OjPzeXoqlL72x", 1),
        ("PL4cUxeGkcC9jLYyp2Aoh6suWpFDbR6E_v", 2),
        ("PLu0W_9lII9agICnT8t4iYVSZ3EnUNzXRm", 3)
    ]

    for p_id, c_id in playlists:
        try:
            request = youtube.playlistItems().list(part='snippet', playlistId=p_id, maxResults=20)
            response = request.execute()
            
            lessons = []
            for item in response.get('items', []):
                lessons.append({
                    "course_id": c_id,
                    "title": item['snippet']['title'],
                    "video_url": f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}",
                    "order_index": item['snippet']['position'] + 1
                })
            
            if lessons:
                supabase.table("lessons").upsert(lessons, on_conflict='video_url').execute()
                print(f"✅ تم رفع {len(lessons)} درس للكورس {c_id}")
        except Exception as e:
            print(f"❌ فشل حقيقي في الكورس {c_id}: {str(e)}")

if __name__ == "__main__":
    start_news_scraping()
    sync_lessons()
    print("🏁 انتهت العملية.")
