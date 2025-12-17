import os
import re
import random
import feedparser
from supabase import create_client, Client
from pytube import Playlist

# 1. إعدادات الربط - استبدل القيم ببياناتك أو GitHub Secrets
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

try:
    supabase: Client = create_client(URL, KEY)
except Exception as e:
    print(f"❌ خطأ في تهيئة Supabase: {e}")

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
    print("✅ تم تحديث الأخبار بنجاح.")

# --- [قسم اليوتيوب: سحب قائمة تشغيل كاملة آلياً] ---

def upload_youtube_playlist(playlist_url):
    print(f"🔄 جاري سحب قائمة التشغيل: {playlist_url}")
    try:
        playlist = Playlist(playlist_url)
        
        # 1. إنشاء الكورس أولاً
        course_data = {
            "title": "كورس فلاتر الشامل - وائل أبو حمزة",
            "thumbnail": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800"
        }
        
        course_response = supabase.table("courses").upsert(course_data, on_conflict='title').execute()
        course_id = course_response.data[0]['id']
        print(f"✅ تم تجهيز الكورس ID: {course_id}")

        # 2. تجهيز الدروس للرفع الجماعي
        lessons_to_upload = []
        for index, video in enumerate(playlist.videos, start=1):
            lesson = {
                "course_id": course_id,
                "title": video.title,
                "video_url": f"https://www.youtube.com/embed/{video.video_id}",
                "order_index": index
            }
            lessons_to_upload.append(lesson)
            print(f"⏳ معالجة درس: {video.title}")

        # 3. رفع الدروس (Upsert لتجنب التكرار إذا كان هناك Key فريد)
        if lessons_to_upload:
            supabase.table("lessons").upsert(lessons_to_upload, on_conflict='video_url').execute()
            print(f"🚀 تم رفع {len(lessons_to_upload)} درس بنجاح!")

    except Exception as e:
        print(f"❌ فشل في سحب اليوتيوب: {e}")

# --- [التشغيل الرئيسي] ---

if __name__ == "__main__":
    # تشغيل سحب الأخبار
    start_news_scraping()
    
    # تشغيل سحب اليوتيوب (كورس وائل أبو حمزة)
    target_playlist = 'https://www.youtube.com/playlist?list=PL93xoRTVf5pZ9m2pP4S7Y_Mv67G90w8fH'
    upload_youtube_playlist(target_playlist)
    
    print("🏁 انتهت جميع العمليات بنجاح.")
