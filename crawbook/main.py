import aiohttp
import asyncio
import random
# import requests
from models import *
from lxml import etree

# https://manybooks.net/search-book?language=All&search=&sort_by=field_downloads
# https://manybooks.net/search-book?language=All&search=&sort_by=field_downloads&page=0  2519

BASE_URL = "https://manybooks.net/search-book?language=All&search=&sort_by=field_downloads&page="
BOOK_URL = "https://manybooks.net"

# asyncio 获取网页信息
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text(encoding='utf-8')

# 下载网页    
async def download(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        return html

# async def download(url):
#     r = requests.get(url)
#     return r.content.decode('utf-8')

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
        Book(**params)

async def down_book(url, errors):
    curl = BOOK_URL+url
    print(curl)
    html = await download(curl)
    html = etree.HTML(html)
    params = {}
    params['title'] = html.xpath("//section[contains(@class,'block-entity-fieldnodefield-t')]/div/div/text()")[-1]
    params['writer'] = html.xpath("/html/body/div[5]/div/div/section/div[2]/div/div[1]/div/div/div[2]/div/section[2]/div/div/div/a/text()")[-1]
    params['published'] = html.xpath("//div[contains(@class,'field--name-field-published-year')]/text()")[-1]
    params['pages'] = html.xpath("//div[contains(@class,'field--name-field-pages')]/text()")[-1]
    params['downloads'] = html.xpath("//div[contains(@class,'field--name-field-downloads')]/text()")[-1]
    params['excerpt'] = html.xpath("//div[contains(@class,'field--name-field-excerpt')]/text()")[-1]
    params['tags'] = html.xpath("//div[contains(@class,'field--name-field-genre')]//a/text()")
    if not params['excerpt'].strip():
        params['excerpt'] = ''.join(html.xpath("//div[contains(@class,'field--name-field-excerpt')]//p/text()"))
    params = {k:v for k,v in params.items() if v}
    print(params,len(params))
    if len(params) < 7:
        errors.append(curl)
    else:
        await save(params)

async def deal_page(url):
    html = await download(url)
    html = etree.HTML(html)
    urls = html.xpath("//div[@class='content']//a/@href")
    errors = []
    for url in urls:
        await down_book(url, errors)
        asyncio.sleep(random.randint(3,8))
    if errors:
        for url in errors:
            await down_book(url, errors)
            asyncio.sleep(random.randint(3,8))

# 利用asyncio模块进行异步IO处理
loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(deal_page(BASE_URL+str(i))) for i in range(1)]
tasks = asyncio.gather(*tasks)
loop.run_until_complete(tasks)