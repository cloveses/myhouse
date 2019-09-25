#!/usr/bin/env python
# coding: utf-8

import time
import requests
from lxml import etree

datafs = []
datass = []

def get_first(url='http://www.shiyebian.net/guizhou/majiangxian/'):
    r = requests.get(url)
    html = r.content.decode('gbk')
    html = etree.HTML(html)
    texts = html.xpath("//div[@class='lie_qx']//h3/strong/a/text()")
    for text in texts:
        print('Current:', text)
    print()
    
    if not datafs:
        datafs.extend(texts)
    else:
        for text in texts:
            if text not in datafs:
                print('New:', text)
        datafs.clear()
        datafs.extend(texts)

def get_second(url='http://www.shiyebian.net/jiaoshi/guizhou/qiandongnan/'):
    r = requests.get(url)
    html = r.content.decode('gbk')
#     print(html[:300])
    html = etree.HTML(html)
    texts = html.xpath("//div[@class='main']/div/ul[@class='lie1']/li/a/text()")
    for text in texts:
        print('Current:', text)
    print()
    
    if not datass:
        datass.extend(texts)
    else:
        for text in texts:
            if text not in datass:
                print('New:', text)
        datass.clear()
        datass.extend(texts)
    

# while True:
#     get_first()
#     get_second()
#     time.sleep(60 * 60 * 8)

if __name__ == '__main__':
    get_first()
    get_second()