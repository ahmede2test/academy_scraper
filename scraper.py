import os
import feedparser
import re
import random
from supabase import create_client
from googleapiclient.discovery import build

# 1. إعدادات الربط (تأكد من إضافتها في GitHub Secrets)
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

supabase = create_client(URL, KEY)
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# --- [وظائف الأخبار] ---

def get_fixed_images():
    """قائمة الصور العشوائية للأخبار"""
    fixed_list = [
        "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&q=80",
        "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800&q=80",
        "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=800&q=80",
        "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800&q=80",
        "https://images.unsplash.com/photo-1587620962725-abab7fe55159?w=800&q=80"
    ]
    random.shuffle(fixed_list)
    return fixed_list

def clean_summary(text):
    if not text: return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace("&nbsp;", " ").strip()
    return text[:250] + "..." if len(text) > 250 else text

def start_news_scraping():
    """سحب الأخبار التقنية ورفعها"""
    sources = [
        {"url": "https://aitnews.com/category/برمجيات-وعلوم-حاسب/feed/", "cat": "برمجيات"},
        {"url": "https://www.tech-wd.com/wd/category/programming/feed/", "cat": "برمجة"},
        {"url": "https://arabhardware.net/news/feed", "cat": "أخبار التقنية"}
    ]
    
    image_pool = get_fixed_images()
    img_ptr = 0
    
    print(f"🚀 بدء سحب الأخبار...")
    for source in sources:
        feed = feedparser.parse(source['url'])
        author = feed.feed.title.split('-')[0].strip() if 'title' in feed.feed else "مصدر تقني"
        
        for entry in feed.entries[:10]:
            current_image = image_pool[img_ptr % len(image_pool)]
            img_ptr += 1

            news_data = {
                "title": entry.title,
                "image_url": current_image,
                "content": clean_summary(entry.summary if 'summary' in entry else entry.title),
                "author": author,
                "category": source['cat']
            }
            
            try:
                supabase.table("academy_news").upsert(news_data, on_conflict='title').execute()
            except Exception as e:
                print(f"⚠️ خطأ في الأخبار: {e}")
    print("✅ تم تحديث الأخبار بنجاح.")

# --- [وظائف الكورسات المحدثة بكشف الأخطاء] ---

def fetch_and_upload_playlist(playlist_id, course_id):
    """يسحب دروس من يوتيوب ويرفعها لجدول lessons مع فحص دقيق للأخطاء"""
    print(f"🔍 محاولة جلب القائمة {playlist_id} للكورس {course_id}...")
    try:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50
        )
        response = request.execute()
        
        if not response.get('items'):
            print(f"⚠️ تحذير: يوتيوب لم يرجع أي فيديوهات لهذه القائمة {playlist_id}!")
            return

        lessons = []
        for item in response['items']:
            lessons.append({
                "course_id": course_id,
                "title": item['snippet']['title'],
                "video_url": f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}",
                "order_index": item['snippet']['position'] + 1
            })
        
        # رفع البيانات (upsert تمنع التكرار بناءً على رابط الفيديو)
        result = supabase.table("lessons").upsert(lessons, on_conflict='video_url').execute()
        print(f"✅ نجاح: تم رفع {len(lessons)} درس لـ Supabase للكورس رقم {course_id}.")
        
    except Exception as e:
        # هنا سيظهر لك السبب الحقيقي لو فشل الرفع (مثلاً مشكلة في API Key أو ID الكورس)
        print(f"❌ خطأ فني في الكورس {course_id}: {str(e)}")

# --- [التشغيل الرئيسي] ---

if __name__ == "__main__":
    # 1. تحديث الأخبار أولاً
    start_news_scraping()
    
    # 2. تحديث الكورسات بالترتيب الصحيح
    # تأكد أن IDs (1, 2, 3) موجودة في جدول courses في سوبابيز
    
    # كورس رقم 1: Dart (Adel Nassim)
    fetch_and_upload_playlist("PL93xoRRE8IsYfVvSnoK_V0Y8f28OEqv92", 1)
    
    # كورس رقم 2: Flutter (Tharwat Samy)
    fetch_and_upload_playlist("PLuYfI_i9-dCdt7w1vK47Y5uO7N5Yf7N8n", 2)
    
    # كورس رقم 3: CS50 بالعربي
    fetch_and_upload_playlist("PLDoPjvoNmBAzS67X-Koxv9n5V9p8nS8C1", 3)
