#!/usr/bin/env python
# coding: utf-8

import time
import requests
from lxml import etree
from email.header import Header
from email.utils import formataddr
import smtplib,base64
from email.mime.text import MIMEText


datafs = []
datass = []

def send_email(content):
    service_email = 'cloveses@126.com'
    receiver = 'cloveses@126.com'
    me = '%s<%s>' % ('cloveses',service_email)
    host = 'smtp.126.com'
    port = 25
    password = ""
    user = 'cloveses'
    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = 'update hint!'
    msg['From'] = formataddr((Header('me', 'utf-8').encode(),service_email))
    msg['To'] = receiver
    msg = msg.as_string()
    try:
        s = smtplib.SMTP(host,port)
        # s = smtplib.SMTP_SSL(host, 465)
        s.set_debuglevel(0)
        s.login(user, password)
        s.sendmail(me,receiver,msg)
        s.quit()
        return True
    except Exception as e:
        print(__file__,':','Do not sendmail,network error')
        print(__file__,':',str(e))
        return False

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
        contents = []
        for text in texts:
            if text not in datafs:
                print('New:', text)
                contents.append(text)
        if contents:
            contents = '\r\n'.join(contents)
            contents = '\r\n'.join([url,contents])
            send_email(contents)
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
        contents = []
        for text in texts:
            if text not in datass:
                print('New:', text)
        if contents:
            contents = '\r\n'.join(contents)
            contents = '\r\n'.join([url,contents])
            send_email(contents)
        datass.clear()
        datass.extend(texts)
    
if __name__ == '__main__':
# while True:
#     get_first()
#     get_second()
#     time.sleep(60 * 60 * 8)
