import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(URL, KEY)

def get_news_from_source(url, selector, source_name):
    headers = {'User-Agent': 'Mozilla/5.0'}
    news_list = []
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.select(selector)[:15] # بنسحب 15 خبر من كل مصدر
        
        for art in articles:
            title_tag = art.find(['h2', 'h3'])
            link_tag = art.find('a')
            img_tag = art.find('img')
            
            if title_tag and link_tag:
                news_list.append({
                    "title": f"[{source_name}] {title_tag.text.strip()}",
                    "image_url": img_tag.get('src') if img_tag else "https://via.placeholder.com/150",
                    "content": f"المصدر: {url}{link_tag['href']}"
                })
        return news_list
    except:
        return []

def scrape_all():
    all_news = []
    # مصدر 1: عرب هاردوير
    all_news += get_news_from_source("https://arabhardware.net/news", "div.post-item", "ArabHardware")
    # مصدر 2: تك وورلد
    all_news += get_news_from_source("https://www.tech-wd.com/wd/category/news/", "article", "TechWD")
    
    if all_news:
        # بنرفع كل الأخبار مرة واحدة
        supabase.table("academy_news").insert(all_news).execute()
        print(f"✅ مبروك! تم إضافة {len(all_news)} خبر جديد.")

if __name__ == "__main__":
    scrape_all()
