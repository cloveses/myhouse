import requests
from bs4 import BeautifulSoup as bsp
import random, time

def get_one_page(url):
    r = requests.get(url)
    soup = bsp(r.text, "html.parser")

    content = soup.find('div',{'class':'mod-bd'})
    Content = content.findAll('span',{'class':'short'})
    Content2 = content.findAll('a',{'href':re.compile('^https://www.douban.com/people'),'class':''})
    for a,b in zip(Content2,Content):
        print(a.string,b.string)

    return Content

def get_all():
    url = ('https://movie.douban.com/subject/26878883/comments?start=','&limit=20&sort=new_score&status=P')
    i = 0
    while True:
        curl = ''.join((url[0],str(i*20),url[-1]))
        time.sleep(random.random()*10)
        datas = get_one_page(curl)
        if not datas:
            break
        print(i)
        i += 1

if __name__ == '__main__':
    get_all()
