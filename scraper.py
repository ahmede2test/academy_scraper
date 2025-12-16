import os
import feedparser
import re
import random
from supabase import create_client

# 1. إعدادات الربط
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(URL, KEY)

def get_100_unique_images():
    """توليد قائمة بـ 100 رابط صورة تقنية فريدة لضمان عدم التكرار"""
    # القائمة الأساسية التي أرسلتها (روابط مباشرة جاهزة)
    base_images = [
        "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&q=80",
        "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800&q=80",
        "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=800&q=80",
        "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800&q=80",
        "https://images.unsplash.com/photo-1587620962725-abab7fe55159?w=800&q=80",
        "https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=800&q=80",
        "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&q=80",
        "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&q=80",
        "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&q=80",
        "https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=800&q=80",
        "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&q=80",
        "https://images.unsplash.com/photo-1534667762233-3b567d6ea065?w=800&q=80",
        "https://images.unsplash.com/photo-1510915228340-29c85a43dcfe?w=800&q=80",
        "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=800&q=80",
        "https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=800&q=80",
        "https://images.unsplash.com/photo-1550439062-609e1531270e?w=800&q=80",
        "https://images.unsplash.com/photo-1580894732444-8ecdead79730?w=800&q=80",
        "https://images.unsplash.com/photo-1551033406-611cf9a28f67?w=800&q=80",
        "https://images.unsplash.com/photo-1484417894907-623942c8ee29?w=800&q=80",
        "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80",
        "https://images.unsplash.com/photo-1562813733-b31f71025d54?w=800&q=80",
        "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800&q=80",
        "https://images.unsplash.com/photo-1536104968055-4d61aa56f46a?w=800&q=80",
        "https://images.unsplash.com/photo-1523961131990-5ea7c61b2107?w=800&q=80",
        "https://images.unsplash.com/photo-1558494949-ef010cbdcc51?w=800&q=80",
        "https://images.unsplash.com/photo-1517139274687-b927132cd2f7?w=800&q=80",
        "https://images.unsplash.com/photo-1516259762381-22954d7d3ad2?w=800&q=80",
        "https://images.unsplash.com/photo-1542744094-3a31f272c490?w=800&q=80",
        "https://images.unsplash.com/photo-1571171637578-41bc2dd41cd2?w=800&q=80",
        "https://images.unsplash.com/photo-1508921234172-b68ed335b3e6?w=800&q=80",
        "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800&q=80",
        "https://images.unsplash.com/photo-1514030849962-49da450429b6?w=800&q=80",
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&q=80",
        "https://images.unsplash.com/photo-1551434678-e076c223a692?w=800&q=80",
        "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&q=80",
        "https://images.unsplash.com/photo-1518433278985-1628127953a1?w=800&q=80",
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&q=80",
        "https://images.unsplash.com/photo-1520085601670-ee14aa58e822?w=800&q=80",
        "https://images.unsplash.com/photo-1537432376769-00f5c2f4c8d2?w=800&q=80",
        "https://images.unsplash.com/photo-1503437313881-503a91226402?w=800&q=80"
    ]
    
    # تكملة القائمة لـ 100 صورة (نضيف 60 صورة إضافية من تصنيفات تقنية)
    tech_topics = ["coding", "cyber", "data", "robot", "server", "tech", "software", "circuit", "web", "ai"]
    for i in range(len(base_images), 100):
        topic = tech_topics[i % len(tech_topics)]
        base_images.append(f"https://images.unsplash.com/featured/?{topic}&sig={i+500}&w=800&q=80")
    
    random.shuffle(base_images) 
    return base_images

def clean_summary(text):
    if not text: return ""
    text = re.sub(r'<[^>]+>', '', text) 
    text = text.replace("&nbsp;", " ").strip()
    return text[:250] + "..." if len(text) > 250 else text

def start_scraping():
    sources = [
        {"url": "https://aitnews.com/category/برمجيات-وعلوم-حاسب/feed/", "cat": "برمجيات"},
        {"url": "https://www.tech-wd.com/wd/category/programming/feed/", "cat": "برمجة"},
        {"url": "https://arabhardware.net/news/feed", "cat": "أخبار التقنية"}
    ]
    
    image_pool = get_100_unique_images()
    img_ptr = 0 
    
    print("🚀 جاري سحب الأخبار وتخصيص صور فريدة...")
    
    for source in sources:
        feed = feedparser.parse(source['url'])
        author = feed.feed.title.split('-')[0].strip() if 'title' in feed.feed else "مصدر تقني"
        
        for entry in feed.entries[:12]:
            current_image = image_pool[img_ptr]
            img_ptr = (img_ptr + 1) % len(image_pool)

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
                print(f"⚠️ خطأ: {e}")
                continue
                
    print(f"✅ تم التحديث! تم استخدام {img_ptr} صورة فريدة.")

if __name__ == "__main__":
    start_scraping()
