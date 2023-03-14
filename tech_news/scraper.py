import requests
import time
from parsel import Selector
from bs4 import BeautifulSoup
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    try:
        time.sleep(1)
        response = requests.get(
            url, timeout=3, headers={"user-agent": "Fake user-agent"},
        )
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
def clean_title(h1):
    if h1.endswith("\xa0\xa0\xa0"):
        h1 = h1[:-len("\xa0\xa0\xa0")]

    return h1


def clean_summary(p):
    if p.endswith("\xa0"):
        p = p[:-len("\xa0")]
    if p.endswith(" "):
        p = p[:-len(" ")]

    return p


def scrape_news(html_content):
    selector = Selector(text=html_content)
    h1 = selector.css("div.entry-header-inner h1::text").get()
    p = BeautifulSoup(
        selector.css("div.entry-content p").get(), "html.parser"
    ).p.text

    return {
        "url": selector.css("head link[rel='canonical']::attr(href)").get(),
        "title": clean_title(h1),
        "timestamp": selector.css("ul li.meta-date::text").get(),
        "writer": selector.css("ul li.meta-author a::text").get(),
        "reading_time": int(
            selector.css("ul li.meta-reading-time::text").get().split(" ")[0]
        ),
        "summary": clean_summary(p),
        "category": selector.css("div.meta-category span.label::text").get(),
    }


# Requisito 5
def get_tech_news(amount):
    url = "https://blog.betrybe.com/"
    list = []
    count = 0

    while count < amount:
        html = fetch(url)
        all_news_links = scrape_updates(html)

        for link in all_news_links:
            if count < amount:
                news_page = fetch(link)
                list.append(scrape_news(news_page))
                count += 1

        url = scrape_next_page_link(html)

    create_news(list)

    return list
