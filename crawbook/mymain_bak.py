import aiohttp
import asyncio
import random
import json
import time
import re
from models_sec import *
from lxml import etree
FBASE_URL = "http://www.gutenberg.org/wiki/Category:Bookshelf"

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

async def fetch_get(session, url):
    asyncio.sleep(random.randint(3,6))
    # print('get:', url)
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
    # print('bookurl:',url)
    book_text = await fetch_get(session, url)
    book_html = etree.HTML(book_text)
    params = {}
    book_seq = url.split('/')[-1]
    if filter(book_seq):
        params['writer'] = book_html.xpath("//table[@class='bibrec']//a[@itemprop='creator']/text()")
        params['title'] = book_html.xpath("//div[@id='content']//h1[@itemprop='name']/text()")
        params['tags'] = book_html.xpath("//table[@class='bibrec']//a[contains(@href,'/browse/loccs')]/text()")
        params['release_date'] = book_html.xpath("//table[@class='bibrec']//td[@itemprop='datePublished']/text()")
        params['downloads'] = book_html.xpath("//table[@class='bibrec']//td[@itemprop='interactionCount']/text()")
        for k,v in params.items():
            if v:
                params[k] = v[-1]
            else:
                params[k] = ''
        params['book_url'] = url.split('/')[-1]
        if 'by' in params['title']:
            params['title'] = params['title'][:params['title'].index('by')].strip()
        # print('params:',params)
        await save(params)
        down_url = book_html.xpath("//div[@id='download']//a[contains(@type,'text/plain')]/@href")
        down_url_html = book_html.xpath("//div[@id='download']//a[contains(@type,'text/html')]/@href")
        # print('down_url:', down_url)
        name = validateTitle(params['title'])
        if not name:
            name = params['book_url']
        name += '.txt'
        if down_url:
            down_url = down_url[0]
            # print('down_url:', down_url)
            if not down_url.startswith('http'):
                down_url = 'http:' + down_url
            async with session.get(down_url) as res:
                text = await res.text(encoding='utf-8')
                with open(name, 'w', encoding='utf-8') as f:
                    f.write(text)
            await save(params)
        elif down_url_html:
            # print('down_url_html:', down_url_html)
            down_url_html = down_url_html[0]
            if not down_url_html.startswith('http'):
                down_url_html = 'http:' + down_url_html
            async with session.get(down_url_html) as res:
                content_text = await res.read()
                content_text = etree.HTML(content_text)
                content_text = content_text.xpath("//body//*/text()")
                if content_text:
                    with open(name, 'w', encoding='utf-8') as f:
                        for txt in content_text:
                            if txt.strip():
                                f.write(txt)
                    await save(params)
        else:
            print('download fail....:', params['book_url'])


@db_session
def save_visited(url):
    Visited(url=url)

@db_session
def ignore_visited(url):
    return exists(u for u in Visited if u.url==url)

def filter_special(url):
    values = ('Help:Logging_in', 'Special:Search', 'Help:Change', '_How-To',
        '_How_should_I_report_them', 'Gutenberg:Contact_Information',
        'wiki/Main_Page', 'Bookshelf_How-To', 'User_talk:')
    for value in values:
        if value in url:
            return True

async def parse(session, url):
    print('url:',url)
    if ignore_visited(url):
        return
    else:
        save_visited(url)
    try:
        shelf_text =  await fetch_get(session, url)
    except:
        print('Failed url:',url)
        return
    shelf_html = etree.HTML(shelf_text)
    book_urls, sub_category_urls = parse_sub(shelf_html)

    for book_url in book_urls:
        try:
            await get_book(session, book_url)
        except:
            print('get book Failed:',book_url)

    sub_category_urls = [u for u in sub_category_urls if not filter_special(u)]
    # print('levels:','\n',book_urls,'\n',sub_category_urls)
    for sub_category_url in sub_category_urls:
        if not sub_category_url.startswith('http'):
            sub_category_url = 'http://www.gutenberg.org' + sub_category_url
        try:
            await parse(session, sub_category_url)
        except:
            print('Category get Failed:',sub_category_url)

async def fetch_main():
    async with aiohttp.ClientSession() as session:
        # 第一次请求获取BOOKSHELF页面
        shelf_text = await fetch_get(session, FBASE_URL)
        shelf_html = etree.HTML(shelf_text)
        main_categories = shelf_html.xpath("//div[@id='mw-subcategories']//a/@href")
        second_categories = shelf_html.xpath("//div[@id='mw-pages']//a[contains(@href,'/wiki/')]/@href")
        main_categories.extend(second_categories)
        second_category_url = shelf_html.xpath("//div[@id='mw-pages']//a[1]/@href")
        if second_category_url:
            second_category_url = second_category_url[0]
            if not second_category_url.startswith('http'):
                second_category_url = 'http:' + second_category_url
            try:
                second_category_text = await fetch_get(session, second_category_url)
                second_category_html = etree.HTML(second_category_text)
                second_categories = second_category_html.xpath("//div[@id='mw-pages']//a[contains(@href,'/wiki/')]/@href")
                main_categories.extend(second_categories)
            except:
                print('second_category_url failed!')
        # print(main_categories) 

        for main_category in main_categories:
            main_category = 'http://www.gutenberg.org' + main_category
            print('main_category', main_category)
            await parse(session, main_category)


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(fetch_main()),]
tasks = asyncio.gather(*tasks)
loop.run_until_complete(tasks)