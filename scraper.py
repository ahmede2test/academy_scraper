import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client

# إعدادات الربط
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(URL, KEY)

def get_news(url, item_selector, title_selector, img_selector, source_name):
    headers = {'User-Agent': 'Mozilla/5.0'}
    results = []
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.select(item_selector)[:10] # يسحب 10 من كل موقع
        
        for art in articles:
            try:
                title = art.select_one(title_selector).text.strip()
                link = art.find('a')['href']
                img = art.select_one(img_selector)
                img_url = img['src'] if img else "https://via.placeholder.com/150"
                
                results.append({
                    "title": f"{title}",
                    "image_url": img_url,
                    "content": f"مصدر الخبر: {source_name} - الرابط: {link}"
                })
            except: continue
        return results
    except: return []

def start_scraping():
    all_found_news = []
    
    # المصدر 1: عرب هاردوير
    all_found_news += get_news("https://arabhardware.net/news", "div.post-item", "h3", "img", "Arab Hardware")
    
    # المصدر 2: تك وورلد (عالم التقنية)
    all_found_news += get_news("https://www.tech-wd.com/wd/category/news/", "article", "h2", "img", "TechWD")
    
    # المصدر 3: أخبار التقنية (اليوم السابع)
    all_found_news += get_news("https://www.youm7.com/Section/%D8%A3%D8%AE%D8%A1%D8%A7%D8%A8%D8%B1-%D0%B0%D9%84%D8%AA%D9%83%D9%86%D9%88%D9%84%D9%88%D8%AC%D9%8A%D8%A7/328/1", "div.big_one_news", "h3", "img", "Youm7 Tech")

    if all_found_news:
        # رفع البيانات (Supabase هيمنع التكرار لو عملت خطوة الـ Unique اللي قلنا عليها)
        for news_item in all_found_news:
            try:
                supabase.table("academy_news").insert(news_item).execute()
            except:
                continue # لو الخبر موجود قبل كدة هيعديه ويشوف اللي بعده
        print(f"✅ تم الانتهاء! حاولنا إضافة {len(all_found_news)} خبر جديد.")

if __name__ == "__main__":
    start_scraping()
