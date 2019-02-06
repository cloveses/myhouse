import aiohttp
import asyncio
import random
import json
import time
import re
# import requests
from models_sec import *
from lxml import etree
# URL    = 'https://manybooks.net/search-book?language=All&field_genre%5B10%5D=10&search=&sort_by=field_downloads'
FBASE_URL = "http://www.gutenberg.org/wiki/Category:Bookshelf"
# "//www.gutenberg.org/ebooks/16460"
# BASE_URL = "https://manybooks.net/search-book?language=All&field_genre%5B{}%5D={}&search=&sort_by=field_downloads&page={}"
# BOOK_URL = "https://manybooks.net"

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

async def fetch_get(session, url):
    asyncio.sleep(random.randint(3,9))
    print('get:', url)
    async with session.get(url) as response:
        return await response.text(encoding='utf-8')

def parse_sub(html):
    categories = html.xpath("//div[@id='mw-content-text']//a[contains(@href,'/wiki/')]/@href")
    books = html.xpath("//div[@id='mw-content-text']//a[contains(@title,'ebook:')]/@href")
    return books,categories

async def save(params):
    params['downloads'] = params['downloads'].split(' ')[0]
    with db_session:
        if hasattr(Book,'writer'):
            Book(**params)

@db_session
def filter(url):
    return not exists(b for b in Book if b.book_url==url)

async def get_book(session, url):
    if not url.startswith('http'):
        url = 'http:' + url
    print('bookurl:',url)
    book_text = await fetch_get(session, url)
    book_html = etree.HTML(book_text)
    params = {}
    book_seq = url.split('/')[-1]
    if filter(book_seq):
        params['writer'] = book_html.xpath("//table[@class='bibrec']//a[@itemprop='creator']/text()")
        params['title'] = book_html.xpath("//div[@id='content']//h1[@itemprop='name']/text()")
        params['tags'] = book_html.xpath("//table[@class='bibrec']//a[contains(@href,'/browse/loccs')]/text()")
        params['release_date'] = book_html.xpath("//table[@class='bibrec']//a[@itemprop='datePublished']/text()")
        params['downloads'] = book_html.xpath("//table[@class='bibrec']//a[@itemprop='interactionCount']/text()")
        for k,v in params.items():
            if v:
                params[k] = v[-1]
            else:
                params[k] = ''
        params['book_url'] = url.split('/')[-1]
        if 'by' in params['title']:
            params['title'] = params['title'][:params['title'].index('by')].strip()
        print('params:',params)
        down_url = book_html.xpath("//div[@id='download']//a[@type='text/plain']/@href")
        down_url_epub = book_html.xpath("//div[@id='download']//a[@type='application/epub+zip']/@href")
        name = validateTitle(params['title'])
        if not name:
            name = params['book_url']
        if down_url:
            down_url = down_url[0]
            if not down_url.startswith('http'):
                down_url = 'http:' + down_url
            name += '.txt'
            async with session.get(down_url) as res:
                text = await res.text(encoding='utf-8')
                with open(name, 'w', encoding='utf-8') as f:
                    f.write(text)
            await save(params)
        elif down_url_epub:
            down_url_epub = down_url_epub[-1]
            if not down_url_epub.startswith('http'):
                down_url_epub = 'http' + down_url_epub
            name += '.epub'
            async with session.get(down_url_epub) as res:
                text = await res.text(encoding='utf-8')
                with open(name, 'w', encoding='utf-8') as f:
                    f.write(text)
            await save(params)
        else:
            print('download fail!')

async def parse(session, url):
    shelf_text =  await fetch_get(session, url)
    shelf_html = etree.HTML(shelf_text)
    book_urls, sub_category_urls = parse_sub(shelf_html)

    for book_url in book_urls:
        await get_book(session, book_url)

    for sub_category_url in sub_category_urls:
        if not sub_category_url.startswith('http'):
            sub_category_url = 'http://www.gutenberg.org' + sub_category_url
        await parse(session, sub_category_url)

async def fetch_main():
    async with aiohttp.ClientSession() as session:
        # 第一次请求获取BOOKSHELF页面
        shelf_text = await fetch_get(session, FBASE_URL)
        shelf_html = etree.HTML(shelf_text)
        main_categories = shelf_html.xpath("//div[@id='mw-subcategories']//a/@href")

        for main_category in main_categories:
            main_category = 'http://www.gutenberg.org' + main_category
            print('main_category', main_category)
            await parse(session, main_category)


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(fetch_main()),]
tasks = asyncio.gather(*tasks)
loop.run_until_complete(tasks)