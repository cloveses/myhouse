# -*- coding: utf-8 -*-

from urllib import parse,request
import json


host = 'http://getlocat.market.alicloudapi.com'
path = '/api/getLocationinfor'
appcode = 'f96f742c99164f0388aa884f44421bd0'
params = {'latlng':'41.93554,118.44361', 'type':2}
url = host + path 

data = parse.urlencode(params).encode(encoding='utf-8')
r = request.Request(url=url, data=data)
r.add_header('Authorization', 'APPCODE ' + appcode)
response = request.urlopen(r)
content = response.read()
if content:
    print(json.loads(content.decode('utf-8')))
