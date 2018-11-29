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

if __name__ == '__main__':
    url = 'https://movie.douban.com/subject/27615439/comments?start=0&limit=20&sort=new_score&status=P'
    get_paget(url)
