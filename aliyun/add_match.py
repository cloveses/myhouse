# -*- coding: utf-8 -*-

from urllib import parse,request
import json


host = 'http://getlocat.market.alicloudapi.com'
path = '/api/getLocationinfor'
method = 'POST'
appcode = 'f96f742c99164f0388aa884f44421bd0'
querys = 'latlng=41.93554%2C118.44361&type=2'
bodys = {}
url = host + path + '?' + querys

request = request.Request(url)
request.add_header('Authorization', 'APPCODE ' + appcode)
response = urllib2.urlopen(request)
content = response.read()
if (content):
    print(content)
