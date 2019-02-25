# -*- coding: utf-8 -*-

from urllib import parse,request
import json


host = 'http://geo.market.alicloudapi.com/v3/geocode/geo'
appcode = 'f96f742c99164f0388aa884f44421bd0'
params = {'address':'北京市朝阳区阜通东大街6号', 'batch':'false', 'callback':'callback','city':'北京', 'output':'JSON'}
data = parse.urlencode(params)
url = ''.join((host, '?', data))
print(url)

r = request.Request(url=url)
r.add_header('Authorization', 'APPCODE ' + appcode)
response = request.urlopen(r)
content = response.read()
if content:
    print(json.loads(content.decode('utf-8')))
