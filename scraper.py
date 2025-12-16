import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client

# سحب البيانات من إعدادات GitHub Secrets (للأمان)
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

if not URL or not KEY:
    print("❌ خطأ: لم يتم العثور على المفاتيح في إعدادات GitHub")
    exit(1)

supabase = create_client(URL, KEY)

def scrape_and_upload():
    print("🚀 بدء سحب الأخبار...")
    target_url = "https://www.tech-wd.com/wd/category/news/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(target_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.select('article')[:5] 
        
        news_to_insert = []
        for art in articles:
            title_tag = art.select_one('h2')
            if title_tag:
                news_to_insert.append({
                    "title": title_tag.text.strip(),
                    "image_url": "https://via.placeholder.com/150", # يمكنك تحسين سحب الصور لاحقاً
                    "content": "تم جلب هذا الخبر آلياً بواسطة نظام الأكاديمية."
                })

        if news_to_insert:
            supabase.table("academy_news").insert(news_to_insert).execute()
            print(f"✅ تم رفع {len(news_to_insert)} خبر بنجاح.")
    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    scrape_and_upload()
