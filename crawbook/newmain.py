import aiohttp
import asyncio
import random
import json
import time
import re
# import requests
from models import *
from lxml import etree
# URL    = 'https://manybooks.net/search-book?language=All&field_genre%5B10%5D=10&search=&sort_by=field_downloads'
FBASE_URL = "https://manybooks.net/search-book?language=All&search=&sort_by=field_downloads&page="
BASE_URL = "https://manybooks.net/search-book?language=All&field_genre%5B{}%5D={}&search=&sort_by=field_downloads&page={}"
BOOK_URL = "https://manybooks.net"

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

async def fetch_get(session, url):
    async with session.get(url) as response:
        return await response.text(encoding='utf-8')

def parse_login_data(html):
    params = {}
    html = etree.HTML(html)
    params['ga_event'] =  html.xpath("//input[@name='ga_event']/@value")[-1]
    params['form_build_id'] = html.xpath("//input[@name='form_build_id']/@value")[-1]
    params['form_id'] = html.xpath("//input[@name='form_id']/@value")[-1]
    params['_triggering_element_name'] = 'op'
    params['_triggering_element_value'] = 'Continue'
    params['_drupal_ajax'] = '1'
    return params

# @db_session
async def save(params):
    for k in ('published', 'pages'):
        if params[k].isdigit():
            params[k] = int(params[k])
        else:
            params[k] = 0
    params['downloads'] = params['downloads'].replace(',','')
    if params['downloads'].isdigit():
        params['downloads'] = int(params['downloads'])
    else:
        params['downloads'] = 0
    params['tags'] = ','.join(params['tags'])
    with db_session:
        try:
            if hasattr(Book,'writer'):
                b = BookInfo(**params)
            else:
                print(Book)
        except:
            pass

# @db_session
async def filter_urls(book_urls):
    new_urls = []
    for book_url in book_urls:
        with db_session:
            if not exists(b for b in Book if b.book_url==book_url):
                new_urls.append(book_url)
    return new_urls

async def parse_book(html, book_url):
    params = {'book_url':book_url}
    title = html.xpath("//section[contains(@class,'block-entity-fieldnodefield-t')]/div/div/text()")
    params['title'] = title[-1] if title else ''
    writer = html.xpath("//a[@itemprop='author']/text()")
    params['writer'] = writer[-1] if writer else ''
    published = html.xpath("//div[contains(@class,'field--name-field-published-year')]/text()")
    params['published'] = published[-1] if published else '0'
    pages = html.xpath("//div[contains(@class,'field--name-field-pages')]/text()")
    params['pages'] = pages[-1] if pages else '0'
    downloads = html.xpath("//div[contains(@class,'field--name-field-downloads')]/text()")
    params['downloads'] = downloads[-1] if downloads else '0'
    params['tags'] = html.xpath("//div[contains(@class,'field--name-field-genre')]//a/text()")
    down_url = html.xpath("//a[@name='download']/@href")
    # print(params)
    # print(down_url)
    if down_url:
        down_url = down_url[-1]
        await save(params)
    else:
        down_url = ''
    return down_url,params['title'] or params['writer']

async def fetch_login():
    async with aiohttp.ClientSession() as session:
        # 第一次请求获取cookie
        async with session.get('https://manybooks.net/') as res:
            # print(res.cookies)
            asyncio.sleep(random.randint(2,5))
        # 第二次请求获取登录信息
        async with session.post('https://manybooks.net/mnybks-login-form?_wrapper_format=drupal_modal') as res:
            # print(res.cookies)
            text = await res.text(encoding='utf-8')
            text = json.loads(text)
            datas = text[-1]['data']
            params = parse_login_data(datas)
            params['ajax_page_state[theme]'] = 'mnybks'
            params['ajax_page_state[theme_token]'] = ''
            params['ajax_page_state[libraries]'] = "bootstrap/popover,bootstrap/tooltip,comment/drupal.comment-by-viewer,core/drupal.autocomplete,core/drupal.dialog.ajax,core/drupal.dialog.ajax,core/html5shiv,google_analytics/google_analytics,mnybks/bootstrap-scripts,mnybks/gleam-script,mnybks/global-styling,mnybks/read-more,mnybks_main/mnybks_main.commands,mnybks_owl/mnybks-owl.custom,mnybks_owl/mnybks-owl.slider,mnybks_seo/mnybks-seo.mouseflow,mnybks_statistic/mnybks_statistic.book-read-statistic-sender,mnybks_statistic/mnybks_statistic.mb-book-stats,paragraphs/drupal.paragraphs.unpublished,system/base,views/views.ajax,views/views.module"
            params['email'] = '45021972@qq.com'
            params['pass'] = 'cloveses'
            # print(params)
        asyncio.sleep(random.randint(12,25))
        #第三次请求登录
        async with session.post('https://manybooks.net/mnybks-login-form?_wrapper_format=drupal_modal&ajax_form=1&_wrapper_format=drupal_ajax',data=params) as res:
            # print(res.cookies['_ga'],res.cookies['_gid'])
            text = await res.text(encoding='utf-8')
            print(text)

        #获取分类
        async with session.get('https://manybooks.net/search-book?language=All&sort_by=field_downloads') as res:
            # print(res.cookies['_ga'],res.cookies['_gid'])
            text = await res.text(encoding='utf-8')
            genre_html = etree.HTML(text)
            genres = genre_html.xpath("//input[contains(@name,'field_genre[')]/@value")
            # print(genres)

        #按分类获取
        for genre in genres:
            genres_urls = []
            page = '0'
            current_url = BASE_URL.format(genre,genre,page)
            genres_urls.append(current_url)
            #获取页数
            async with session.get(current_url) as res:
                # print(res.cookies['_ga'],res.cookies['_gid'])
                text = await res.text(encoding='utf-8')
                pagenum_html = etree.HTML(text)
                page_num = pagenum_html.xpath('//a[@title="Go to last page"]/@href')
                if page_num:
                    page_num = page_num[-1]
                    page_num = page_num[page_num.index('page=') + len('page='):]
                    page_num = int(page_num) + 1
                    for i in range(1,page_num):
                        genres_urls.append(BASE_URL.format(genre,genre,str(i)))
            # print(genres_urls)

            #获取某目录页中所有书
            for outline_page_url in genres_urls:
                outline_html = await fetch_get(session, outline_page_url)
                outline_html = etree.HTML(outline_html)
                outline_urls = outline_html.xpath("//div[@class='content']//a/@href")
                outline_urls = await filter_urls(outline_urls)
                asyncio.sleep(random.randint(3,12))
                # 获取每本书信息
                for book_url in outline_urls:
                    print(book_url)
                    book_url = BOOK_URL + book_url
                    try:
                        book_html = await fetch_get(session, book_url)
                    except:
                        continue
                    book_html = etree.HTML(book_html)
                    down_url,title = await parse_book(book_html, book_url[len(BOOK_URL):])
                    if down_url:
                        # print(down_url,title)
                        asyncio.sleep(random.randint(3,12))
                        title = validateTitle(title)
                        if not title:
                            title = validateTitle(book_url)
                        async with session.get(BOOK_URL+down_url) as res:
                            text = await res.text(encoding='utf-8')
                            with open(title + '.txt', 'w', encoding='utf-8') as f:
                                f.write(text)


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(fetch_login()),]
tasks = asyncio.gather(*tasks)
loop.run_until_complete(tasks)