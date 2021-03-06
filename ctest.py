import requests
from bs4 import BeautifulSoup as bsp
import random, time, re

def get_page(url):
    r = requests.get(url)
    mysoup = bsp(r.text, "html.parser")

    content = mysoup.find('div',{'class':'mod-bd'})
    Content = content.findAll('span',{'class':'short'})
    authors = content.findAll('a',{'href':re.compile('^https://www.douban.com/people'),'class':''})
    for a,b in zip(authors[1::2],Content):
        try:
            print(a.string,'的短评：\n',b.string)
        except:
            pass

    return Content

def get_content():
    url = ('https://movie.douban.com/subject/27615439/comments?start=','&limit=20&sort=new_score&status=P')
    page = 0
    while True:
        curl = ''.join((url[0],str(page*20),url[-1]))
        time.sleep(random.random()*10)
        datas = get_page(curl)
        if not datas :
            break
        page += 1

if __name__ == '__main__':
    get_content()
