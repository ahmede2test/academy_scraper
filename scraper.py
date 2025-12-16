import os
import feedparser
import re
import openai  # تأكد من إضافة openai للملف requirements.txt
from supabase import create_client

# الإعدادات
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

supabase = create_client(URL, KEY)
client = openai.OpenAI(api_key=OPENAI_KEY)

def get_ai_image_prompt(title):
    """استخدام OpenAI لوصف صورة احترافية تناسب الخبر"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a creative image prompt engineer. Translate the news title to English and provide 3 keywords for high-quality technology photography."},
                {"role": "user", "content": title}
            ]
        )
        keywords = response.choices[0].message.content.strip()
        # نستخدم الكلمات الناتجة لجلب صورة دقيقة من Unsplash
        return f"https://source.unsplash.com/featured/800x600/?{keywords.replace(' ', ',')}"
    except:
        # fallback في حال فشل الـ API
        return f"https://source.unsplash.com/featured/800x600/?technology,coding&sig={hash(title)}"

def start_scraping():
    sources = [
        {"url": "https://aitnews.com/category/برمجيات-وعلوم-حاسب/feed/", "cat": "برمجيات"},
        {"url": "https://www.tech-wd.com/wd/category/programming/feed/", "cat": "برمجة"}
    ]
    
    for source in sources:
        feed = feedparser.parse(source['url'])
        for entry in feed.entries[:10]:
            # الذكاء الاصطناعي يحدد أفضل صورة
            img_url = get_ai_image_prompt(entry.title)
            
            # تلخيص المحتوى بواسطة AI ليصبح احترافياً (اختياري)
            content_clean = re.sub(r'<[^>]+>', '', entry.summary)[:200] + "..."

            news_data = {
                "title": entry.title,
                "image_url": img_url,
                "content": content_clean,
                "author": "محرر الذكاء الاصطناعي",
                "category": source['cat']
            }
            supabase.table("academy_news").upsert(news_data, on_conflict='title').execute()

if __name__ == "__main__":
    start_scraping()
