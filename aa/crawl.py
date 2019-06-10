# -*- coding: utf-8 -*-

payload = {"userName":"********","password":"*******","ValidateCode":""}
import requests
from lxml import html

url = 'http://elite.nju.edu.cn/jiaowu/'

img_url = url+"ValidateCode.jsp"
img = requests.get(img_url,stream=True)
with open("checkcode.gif",'wb') as f:
    f.write(img.content)

from PIL import Image
image = Image.open("checkcode.gif") 
image.show() 
checkcode = input("input checkcode:") 
payload['ValidateCode'] = checkcode



session_requests = requests.session()

result = session_requests.get(url)
tree = html.fromstring(result.text)
authenticity_token = list(set(tree.xpath("//input[@name='returnUrl']/@value")))[0]
result = session_requests.post(url,data = payload,headers = dict(referer=url))

# __Author__ = 'Kasphysm'

# import config
# from urllib import request, parse
# from http import cookiejar
# import re

# targetPath = config.targetPath
# url = 'http://elite.nju.edu.cn/jiaowu/student/index.do'
# url_login = 'http://elite.nju.edu.cn/jiaowu/login.do'
# url_CAPTCHA = 'http://elite.nju.edu.cn/jiaowu/ValidateCode.jsp'
# url_my_course = 'http://elite.nju.edu.cn/jiaowu/student/teachinginfo/courseList.do?method=currentTermCourse'
# url_all_course = 'http://elite.nju.edu.cn/jiaowu/student/teachinginfo/allCourseList.do?method=getTermAcademy'
# url_academy_course = 'http://elite.nju.edu.cn/jiaowu/student/teachinginfo/allCourseList.do?method=getCourseList'
# headers = config.headers

# class crawler():
    
#     def __init__(self):
#         self.create_opener()
        
#     def create_opener(self):
#         cookie_support = request.HTTPCookieProcessor(cookiejar.CookieJar())
#         global opener
#         opener = request.build_opener(cookie_support, request.HTTPHandler)

#     def get_CAPTCHA(self):
#         img_CAPTCHA = opener.open(url_CAPTCHA).read()
#         f = open(targetPath+'\\Img_CAPTCHA.jpg', 'wb')
#         f.write(img_CAPTCHA)
#         f.close()

#     def login(self, acc, pwd, CAPTCHA):
#         data = {'userName': acc,
#                 'password': pwd,
#                 'returnUrl': 'null',
#                 'ValidateCode': CAPTCHA}
#         post_data = parse.urlencode(data).encode('utf-8')
#         req = request.Request(url_login, headers = headers, data = post_data)
#         #opener.open(req)
#         resp = opener.open(req)
#         return resp

#     def get_all_course(self, term, grade, academy):
#         req = request.Request(url_academy_course+'&curTerm='+term+'&curSpeciality='+academy+'&curGrade='+grade,
#                               headers = headers)
#         resp = opener.open(req)
#         content = resp.read().decode('utf-8')
#         reObj_course = re.compile(u'.*?<td align="center" valign="middle">(.*?)</td>.*?\n'
#                                   +u'.*?<td valign="middle">(.*?)</td>.*?\n'
#                                   +u'.*?<td align="center" valign="middle">(.*?)</td>.*?\n'
#                                   +u'.*?<td align="center" valign="middle">(.*?)</td>.*?\n'
#                                   +u'.*?<td align="center" valign="middle">(.*?)</td>.*?\n'
#                                   +u'.*?<td align="center" valign="middle">(.*?)</td>.*?\n'
#                                   +u'.*?<td align="center" valign="middle">(.*?)</td>.*?\n'
#                                   +u'.*?<td valign="middle">(.*?)</td>.*?\n'
#                                   +u'.*?<td valign="middle">(.*?)</td>'
#                                   +u'.*?')
#         raw_data = reObj_course.findall(content)
#         return raw_data