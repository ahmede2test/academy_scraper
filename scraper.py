import os
import feedparser
import re
import random
from supabase import create_client
from googleapiclient.discovery import build

# 1. إعدادات الربط (تأكد من وجودها في GitHub Secrets)
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

supabase = create_client(URL, KEY)
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# --- [وظائف الأخبار] ---

def get_fixed_images():
    """قائمة صور عشوائية للأخبار لضمان شكل جذاب"""
    fixed_list = [
        "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800",
        "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800",
        "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=800",
        "https://images.unsplash.com/photo-1587620962725-abab7fe55159?w=800"
    ]
    random.shuffle(fixed_list)
    return fixed_list

def clean_summary(text):
    if not text: return ""
    text = re.sub(r'<[^>]+>', '', text) # حذف وسوم HTML
    text = text.replace("&nbsp;", " ").strip()
    return text[:250] + "..." if len(text) > 250 else text

def start_news_scraping():
    """سحب الأخبار التقنية ورفعها لجدول academy_news"""
    sources = [
        {"url": "https://aitnews.com/category/برمجيات-وعلوم-حاسب/feed/", "cat": "برمجيات"},
        {"url": "https://www.tech-wd.com/wd/category/programming/feed/", "cat": "برمجة"}
    ]
    image_pool = get_fixed_images()
    img_ptr = 0
    print("🚀 بدء سحب الأخبار...")
    for source in sources:
        feed = feedparser.parse(source['url'])
        for entry in feed.entries[:8]:
            news_data = {
                "title": entry.title,
                "image_url": image_pool[img_ptr % len(image_pool)],
                "content": clean_summary(entry.summary if 'summary' in entry else entry.title),
                "author": "مصدر تقني",
                "category": source['cat']
            }
            img_ptr += 1
            try:
                supabase.table("academy_news").upsert(news_data, on_conflict='title').execute()
            except Exception as e:
                print(f"⚠️ خطأ خبر: {e}")
    print("✅ تم تحديث الأخبار بنجاح.")

# --- [وظائف الكورسات والدروس] ---

def sync_lessons():
    """تحديث الكورسات والدروس مع ميزة الإصلاح الذاتي للـ IDs"""
    print("🔄 جاري فحص الكورسات والدروس...")
    
    # خطوة هامة: التأكد من وجود الكورسات 1 و 2 و 3 في سوبابيز أولاً لتجنب خطأ الربط
    courses_to_ensure = [
        {"id": 1, "title": "CS50 - علوم الحاسب"},
        {"id": 2, "title": "Flutter - تطوير تطبيقات"},
        {"id": 3, "title": "Python - لغة بايثون"}
    ]
    for c in courses_to_ensure:
        supabase.table("courses").upsert(c).execute()

    # قوائم التشغيل (Playlists) المستهدفة
    playlists = [
        ("PLDoPjvoNmBAw6p0z0Ek0OjPzeXoqlL72x", 1), # CS50
        ("PL4cUxeGkcC9jLYyp2Aoh6suWpFDbR6E_v", 2), # Flutter
        ("PLu0W_9lII9agICnT8t4iYVSZ3EnUNzXRm", 3)  # Python
    ]

    for p_id, c_id in playlists:
        try:
            print(f"🔍 فحص دروس القائمة: {p_id}")
            request = youtube.playlistItems().list(
                part='snippet',
                playlistId=p_id.strip(),
                maxResults=50
            )
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
                print(f"✅ نجاح: تم رفع {len(lessons)} درس للكورس {c_id}")
        
        except Exception as e:
            print(f"❌ فشل في جلب دروس الكورس {c_id}: {e}")

# --- [التشغيل الرئيسي] ---

if __name__ == "__main__":
    # 1. تحديث قسم الأخبار
    start_news_scraping()
    
    # 2. تحديث قسم الدروس
    sync_lessons()
    
    print("🏁 اكتملت جميع العمليات بنجاح!")
