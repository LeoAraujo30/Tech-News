import requests
import time
from parsel import Selector


# Requisito 1
def fetch(url):
    try:
        time.sleep(1)
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.ReadTimeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(text=html_content)
    list = selector.css("div.post-outer h2 a::attr(href)").getall()
    return list


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    link = selector.css("div.nav-links a.next::attr(href)").get()
    if link:
        return link
    else:
        return None


# Requisito 4
def scrape_news(html_content):
    selector = Selector(text=html_content)
    dict = {
        "url": selector.css("head link[rel='canonical']::attr(href)").get(),
        "title": selector.css("div.entry-header-inner h1::text").get(),
        "timestamp": selector.css("ul li.meta-date::text").get(),
        "writer": selector.css("ul li.meta-author a::text").get(),
        "reading_time": int(
            selector.css("ul li.meta-reading-time::text").get().split(" ")[0]
        ),
        "summary": selector.css("div.entry-content p *::text").get(),
        "category": selector.css("div.meta-category span.label::text").get(),
    }
    print(dict)
    return dict


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
