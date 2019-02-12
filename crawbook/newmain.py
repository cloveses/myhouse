import aiohttp
import asyncio
import random
import json
import time
import re
from models import *
from lxml import etree
# URL    = 'https://manybooks.net/search-book?language=All&field_genre%5B10%5D=10&search=&sort_by=field_downloads'
# FBASE_URL = "https://manybooks.net/search-book?language=All&search=&sort_by=field_downloads&page="
# BASE_URL = "https://manybooks.net/search-book?language=All&field_genre%5B{}%5D={}&search=&sort_by=field_downloads&page={}"
MAIN_URL = "https://manybooks.net"
FSEARCH_URL = "https://manybooks.net/search-book?search=&ga_submit={}"
SEARCH_URL = "https://manybooks.net/search-book?search=&ga_submit={}&language=All&sort_by=field_downloads&page={}"

sem = asyncio.Semaphore(30)

@db_session
def save_url(urls):
    for url in set(urls):
        # print('url:', url)
        if url.startswith('/titles') and url.endswith('.html') and\
            not exists(b for b in Book_v2 if b.book_url==url) and \
            not exists(b for b in Book if b.book_url==url):
            Book_v2(book_url=url)

async def fetch_get(session, url):
    async with sem:
        async with session.get(url) as response:
            return await response.text(encoding='utf-8')

async def get_book_urls(session, url):
    async with sem:
        text = await fetch_get(session, url)
        html = etree.HTML(text)
        urls = html.xpath("//div[@class='content']//a/@href")
        save_url(urls)

async def main():
    async with sem:
        async with aiohttp.ClientSession() as session:
            # 第一次请求获取params
            main_text = await fetch_get(session, MAIN_URL)
            main_html = etree.HTML(main_text)
            params = {}
            params['form_build_id'] = main_html.xpath("//input[@name='form_build_id']/@value")
            params['form_id'] = main_html.xpath("//input[@name='form_id']/@value")
            params['op'] = main_html.xpath("//button[@id='edit-submit']/@value")
            params['ga_submit'] = main_html.xpath("//input[@name='ga_event']/@value")
            for k,v in params.items():
                if v:
                    params[k] = v[0]
                else:
                    print('No params!')
                    return
            params['search'] = ''

            # 第二次POST请求
            async with session.post('https://manybooks.net/search-book',data=params) as res:
                pass

            fsearch_text = await fetch_get(session, FSEARCH_URL.format(params['ga_submit']))
            fsearch_html = etree.HTML(fsearch_text)
            page_num = fsearch_html.xpath('//a[@title="Go to last page"]/@href')[0]
            page_num = int(page_num[page_num.index('page=')+len('page='):])
            print(page_num)

            foutline_urls = fsearch_html.xpath("//div[@class='content']//a/@href")
            save_url(foutline_urls)

            tasks = []
            for page in range(1, page_num+1): # page_num+1
                search_url = SEARCH_URL.format(params['ga_submit'],page)
                print(search_url)
                tasks.append(asyncio.ensure_future(get_book_urls(session,search_url)))
            tasks.append(asyncio.ensure_future(fetch_login()))
            return await asyncio.gather(*tasks)

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

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

async def save(params, book_url):
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
        book = select(b for b in Book_v2 if b.book_url==book_url).first()
        if book:
            for k,v in params.items():
                setattr(book, k, v)
            book.visited = 1
        else:
            print('update error:', book_url)
        # try:
        #     if hasattr(Book_v2,'writer'):
        #         b = Book_v2(**params)
        #     else:
        #         print(Book_v2)
        # except:
        #     pass

async def parse_book(html, book_url):
    params = {}
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
        await save(params, book_url)
    else:
        down_url = ''
    return down_url,params['title'] or params['writer']

async def get_one_book(session, book_url):
    async with sem:
        print(book_url)
        book_url = MAIN_URL + book_url
        try:
            book_html = await fetch_get(session, book_url)
        except:
            print('failed book_url:',book_url)
            return
        book_html = etree.HTML(book_html)
        down_url,title = await parse_book(book_html, book_url[len(MAIN_URL):])
        if down_url:
            print(down_url,title)
            asyncio.sleep(random.randint(1,4))
            title = validateTitle(title)
            if not title:
                title = validateTitle(book_url)
            try:
                async with session.get(MAIN_URL+down_url) as res:
                    text = await res.text(encoding='utf-8')
                    with open(title + '.txt', 'w', encoding='utf-8') as f:
                        f.write(text)
            except:
                print('field_downloads:', MAIN_URL+down_url)

async def fetch_login():
    # asyncio.sleep(120)
    async with sem:
        async with aiohttp.ClientSession() as session:
            # 第一次请求获取cookie
            async with session.get('https://manybooks.net') as res:
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
                params['email'] = 'cloveses@126.com' # '45021972@qq.com'
                params['pass'] = 'cloveses'
                # print(params)
            asyncio.sleep(random.randint(2,5))
            #第三次请求登录
            async with session.post('https://manybooks.net/mnybks-login-form?_wrapper_format=drupal_modal&ajax_form=1&_wrapper_format=drupal_ajax',data=params) as res:
                # print(res.cookies['_ga'],res.cookies['_gid'])
                text = await res.text(encoding='utf-8')
                print(text)

                # 获取每本书信息
            counts = 1
            while True:
                books = None
                with db_session:
                    books = select(b for b in Book_v2 if b.visited==0)[:20]
                if not books and counts >= 6000:
                    break
                elif not books :
                    asyncio.sleep(counts * 2)
                    counts += 1
                    continue
                else:
                    tasks = []
                    for book in books:
                        print('add task:', book.book_url)
                        tasks.append(asyncio.ensure_future(get_one_book(session, book.book_url)))
                    await asyncio.gather(*tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    # loop.run_until_complete(fetch_login())
