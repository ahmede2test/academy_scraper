import os
import feedparser
import re
from supabase import create_client

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(URL, KEY)

def extract_best_image(entry):
    """دالة ذكية لاستخراج أفضل رابط صورة متاح للخبر"""
    # 1. محاولة البحث في وسم media_content
    if 'media_content' in entry and len(entry.media_content) > 0:
        return entry.media_content[0]['url']
    
    # 2. محاولة البحث في الروابط (Enclosures)
    if 'links' in entry:
        for link in entry.links:
            if 'image' in link.get('type', ''):
                return link.href

    # 3. البحث داخل الوصف أو المحتوى باستخدام Regex (الأكثر دقة للمواقع العربية)
    search_text = ""
    if 'content' in entry:
        search_text = entry.content[0].value
    elif 'summary' in entry:
        search_text = entry.summary
    
    if search_text:
        # البحث عن أول رابط ينتهي بامتداد صورة
        match = re.search(r'src="([^"]+\.(?:jpg|png|jpeg|webp|gif)[^"]*)"', search_text)
        if match:
            return match.group(1)

    # 4. صورة افتراضية "متغيرة" تعتمد على عنوان الخبر لضمان عدم التكرار
    # نستخدم sig لجعل Unsplash يعطي صورة مختلفة لكل خبر
    return f"https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=1000&sig={hash(entry.title)}"

def start_scraping():
    sources = [
        {"url": "https://aitnews.com/category/برمجيات-وعلوم-حاسب/feed/", "cat": "برمجيات"},
        {"url": "https://www.tech-wd.com/wd/category/programming/feed/", "cat": "برمجة"},
        {"url": "https://www.unlimit-tech.com/category/programming/feed/", "cat": "تطوير"}
    ]
    
    print("🚀 جاري بدء سحب الأخبار بصورها الأصلية...")
    
    for source in sources:
        feed = feedparser.parse(source['url'])
        # استخراج اسم الموقع بشكل أنظف
        author_name = feed.feed.title.split('-')[0].strip() if 'title' in feed.feed else "مصدر تقني"
        
        for entry in feed.entries[:15]:
            # استخدام الدالة الجديدة لجلب الصورة الحقيقية
            img_url = extract_best_image(entry)

            # تنظيف المحتوى من وسوم HTML تماماً
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
                # تحديث لو العنوان موجود أو إضافة لو جديد
                supabase.table("academy_news").upsert(news_data, on_conflict='title').execute()
            except Exception as e:
                print(f"❌ خطأ في رفع خبر: {entry.title[:20]}... : {e}")
                continue
                
    print("✅ تم التحديث بنجاح! الصور الآن يجب أن تكون متنوعة.")

if __name__ == "__main__":
    start_scraping()
