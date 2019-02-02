import aiohttp
import asyncio


# https://manybooks.net/search-book?language=All&search=&sort_by=field_downloads
# https://manybooks.net/search-book?language=All&search=&sort_by=field_downloads&page=0  2519


# asyncio 获取网页信息
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text(encoding='gb18030')

# 解析网页
async def parser_catalogue(html):
    # 返回
    pass

async def parser_book(html):
    pass

# 处理网页    
async def download(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        await parser(html)

urls = []

# 利用asyncio模块进行异步IO处理
loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(download(url)) for url in urls]
tasks = asyncio.gather(*tasks)
loop.run_until_complete(tasks)