import requests
from bs4 import BeautifulSoup as bsp
import random, time, re
from selenium import webdriver

br = webdriver.Firefox()
datas = []
start = 0
purl ='https://zh.airbnb.com/s/Shenzhen--China/homes?refinement_paths%5B%5D=%2Fhomes&click_referer=t%3ASEE_ALL%7Csid%3A2b85debd-47d2-4ada-8ca8-fcc0db9ee568%7Cst%3AMATCHA_HOME_WITH_POPULAR_AMENITY&amenities%5B%5D=8&title_type=NONE&query=Shenzhen%2C%20China&allow_override%5B%5D=&s_tag=GsyU9pJ-&section_offset=6&items_offset=90'
# while True:
#     if start:
#         url_parts = '&section_offset=6&items_offset=%d' % start * 18
br.get(purl)
time.sleep(35)
mysoup = bsp(br.page_source,"html.parser")
content = mysoup.find('main',{'id':'site-content'})
# print(content)
urls = content.findAll('a',{'href':re.compile('^/rooms/')})
# print(urls)
try:
    for url in urls[:3]:
        # print()
        roomurl = url.get('href')
        br.get('https://zh.airbnb.com'+roomurl)
        time.sleep(5)
        aa = br.find_element_by_xpath('/html/body/div[4]/div/main/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[2]/div/div/div/div[1]/div/div/div[2]/div/div[1]/span').text
        bb = br.find_element_by_xpath('/html/body/div[4]/div/main/div/div/div[2]/div/div/div[1]/div[2]/div/div/div/div/div[1]/div/div/div[1]/div/div/div[2]/div[1]/span/div/div/div/span[1]/span').text
        cc = br.find_element_by_xpath('/html/body/div[4]/div/main/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[2]/div/div/div/div[2]/div[1]/div/div[1]/div/div/p/span').text
        dd = br.find_element_by_xpath('/html/body/div[4]/div/main/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[6]/div/div/div/section').text
        ee = br.find_element_by_xpath('/html/body/div[4]/div/main/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[7]/div/div/section/div').text
        ff = br.find_element_by_xpath('/html/body/div[4]/div/main/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/section/div[2]/div[3]').text
        datas.append((aa,bb,cc,dd,ee,ff))
        print(aa,bb,cc,dd,ee,ff)
except:
    print('error',url)
with open('data.txt','w',encoding='utf-8') as f:
    for data in datas:
        for d in data:
            f.write(d)
            f.write('\n')
        f.write('\n')
