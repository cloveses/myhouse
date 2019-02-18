import aiohttp
import asyncio
import random
import json
import time
import re
import os
from v2models import *
from lxml import etree
# URL    = 'https://manybooks.net/search-book?language=All&field_genre%5B10%5D=10&search=&sort_by=field_downloads'
# FBASE_URL = "https://manybooks.net/search-book?language=All&search=&sort_by=field_downloads&page="
# BASE_URL = "https://manybooks.net/search-book?language=All&field_genre%5B{}%5D={}&search=&sort_by=field_downloads&page={}"
MAIN_URL = "https://manybooks.net"
FSEARCH_URL = "https://manybooks.net/search-book?search=&ga_submit={}"
SEARCH_URL = "https://manybooks.net/search-book?search=&ga_submit={}&language=All&sort_by=field_downloads&page={}"
TOTALS = 0
TIMES_LOGIN = 4000

sem = asyncio.Semaphore(30)

@db_session
def save_url(urls):
    # print('目录页URL：',set(urls))
    for url in set(urls):
        # print('url:', url)
        if url.startswith('/titles') and url.endswith('.html') and\
            not exists(b for b in Book if b.book_url==url):
            Book(book_url=url)

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

#获取目录页中书的URL
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
            # #test
            # page_num = 3
            global TOTALS
            TOTALS = page_num * 24
            foutline_urls = fsearch_html.xpath("//div[@class='content']//a/@href")
            save_url(foutline_urls)

            tasks = []
            part_tasks = []
            start = 0
            for page in range(start, page_num+1): # page_num+1
                if page % 15 == 0:
                    asyncio.sleep(240)
                    part_tasks = []
                search_url = SEARCH_URL.format(params['ga_submit'],page)
                print(search_url)
                task = asyncio.ensure_future(get_book_urls(session,search_url))
                part_tasks.append(task)
                tasks.append(task)
                if page % 15 == 0:
                    await asyncio.wait(part_tasks)
                    await asyncio.sleep(25)
                if page == start + 10:
                    #添加获取书内容的任务
                    tasks.append(asyncio.ensure_future(fetch_main()))
            #添加再次获取下载的文本文件内容为空的任务
            # tasks.append(asyncio.ensure_future(fetch_again()))
            await asyncio.wait(tasks)

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

@db_session
def quit():
    if count(c for c in Book) >= TOTALS - 24 and count(c for c in Book if c.visited==0) <= 0:
    # #test
    # if count(c for c in Book) >= 35 and count(c for c in Book if c.visited==0) <= 0:
        return True

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

#保存书籍的相关数据
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
        book = select(b for b in Book if b.book_url==book_url).first()
        if book:
            for k,v in params.items():
                setattr(book, k, v)
            book.visited = 1
        else:
            print('update error:', book_url)

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
        params['down_url'] = down_url
        await save(params, book_url)
    else:
        down_url = ''
    return down_url,params['title'] or params['writer']

#获取一本书的信息及内容
async def get_one_book(session, book_url):
    async with sem:
        print('get book:', book_url)
        file_name = book_url.split('/')[-1]
        if file_name.endswith('.html'):
            file_name = file_name[:-5] + '_html'
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
            file_name = ''.join((down_url.split('/')[-2], '_', file_name, '.txt'))
            file_name = validateTitle(file_name)
            try:
                async with session.get(MAIN_URL+down_url) as res:
                    text = await res.text(encoding='utf-8')
                    with open(file_name, 'w', encoding='utf-8') as f:
                        f.write(text)
            except:
                print('field_downloads:', MAIN_URL+down_url)

# 获取目录下内容为空的文件
@db_session
def get_empty_files():
    files = os.listdir()
    files = [os.path.splitext(f)[0] for f in files if os.path.isfile(f) and os.lstat(f).st_size == 0]
    # /books/get/126812/8
    book_urls = [('/'.join(('/books/get',f.split('_')[0],'8')),f) for f in files]
    return book_urls

async def get_one_book_txt(session, down_url, file_name):
    async with sem:
        if down_url:
            asyncio.sleep(random.randint(1,4))
            file_name += '.txt'
            try:
                async with session.get(MAIN_URL+down_url) as res:
                    text = await res.text(encoding='utf-8')
                    with open(file_name, 'w', encoding='utf-8') as f:
                        f.write(text)
            except:
                print('field_downloads:', MAIN_URL+down_url)

async def fetch_again(session):
    tasks = []
    books = get_empty_files()
    print('empty files:',books)
    for book in books:
        tasks.append(asyncio.ensure_future(get_one_book_txt(session, book[0], book[1])))
    await asyncio.wait(tasks)
    await asyncio.sleep(25)

async def fetch_main():
    userdatas = [('dingaa@126.com', 'dingaa'), ('dingbb@126.com', 'dingbb'),('45021972@qq.com', 'cloveses')]
    i = 0
    while True:
        if quit():
            break
        await fetch_login(userdatas[i%3])
        print('sleep 5 minutes...')
        await asyncio.sleep(5 * 60)
        i += 1

#登录后获取书
async def fetch_login(userdata):
    # asyncio.sleep(120)
    totals = 0
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
                # params['email'] = '45021972@qq.com' # '45021972@qq.com'
                # params['pass'] = 'cloveses'
                # params['email'] = 'dingaa@126.com' # '45021972@qq.com'
                # params['pass'] = 'dingaa'
                params['email'] = userdata[0]
                params['pass'] = userdata[1]
                print('login info:', params)
            asyncio.sleep(random.randint(2,5))
            #第三次请求登录
            async with session.post('https://manybooks.net/mnybks-login-form?_wrapper_format=drupal_modal&ajax_form=1&_wrapper_format=drupal_ajax',data=params) as res:
                # print(res.cookies['_ga'],res.cookies['_gid'])
                text = await res.text(encoding='utf-8')
                print(text)
            print('登录成功...')
                # 获取每本书信息
            counts = 1
            while True:
                if quit() or totals >= TIMES_LOGIN:
                    break
                asyncio.sleep(30)
                books = None
                with db_session:
                    books = select(b for b in Book if b.visited==0)[:10]
                if not books:
                    asyncio.sleep(counts * 2)
                    if counts < 60:
                        counts += 1
                    continue
                else:
                    tasks = []
                    for book in books:
                        totals += 1
                        # print('add task:', book.book_url)
                        tasks.append(asyncio.ensure_future(get_one_book(session, book.book_url)))
                    await asyncio.wait(tasks)
                    await asyncio.sleep(25)
            if totals < TIMES_LOGIN:
                await fetch_again(session)
                await asyncio.sleep(25)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    # loop.run_until_complete(fetch_login())
