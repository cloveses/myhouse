import aiohttp
import asyncio
import random
import json
import time
import re
from models_sec import *
from lxml import etree
FBASE_URL = "http://www.gutenberg.org/ebooks/"

sem = asyncio.Semaphore(30)

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

async def fetch_get(session, url):
    async with sem:
        asyncio.sleep(random.randint(1,5))
        print('get:', url)
        async with session.get(url) as response:
            return await response.text(encoding='utf-8')

async def save(params):
    params['downloads'] = params['downloads'].split(' ')[0]
    with db_session:
        if hasattr(Book,'writer'):
            Book(**params)

@db_session
def filter(url):
    return not exists(b for b in Book if b.book_url==url)

async def get_book(session, url):
    # print('bookurl:',url)
    book_text = await fetch_get(session, url)
    book_html = etree.HTML(book_text)
    params = {}
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
    if os.path.exists(name + '.txt'):
        name += '_1'
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


async def fetch_main():
    async with sem:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(1,58803):
                istr = str(i)
                if filter(istr):
                    tasks.append(asyncio.ensure_future(get_book(session, FBASE_URL+istr)))
                if i % 50 == 0:
                    asyncio.sleep(120)
            await asyncio.wait(tasks)


if  __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_main())