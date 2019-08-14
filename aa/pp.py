import re
import time
from selenium import webdriver

br = webdriver.Firefox()
br.get('http://ping.chinaz.com/www.baidu.com')
br.implicitly_wait(60)
while True:
    cc = br.find_element_by_xpath("//ul/li[@class='item']")
    ds = re.findall(r'\d+', cc.text)
    if ds and ds[0] == ds[-1]:
        break
    else:
        time.sleep(30)

containers = br.find_elements_by_xpath("//div[@id='speedlist']/div")
datas = []
for c in containers[1:]:
    datas.append(c.text.split('\n')[:-1])

for data in datas:
    print(data)

datas = [','.join(d) for d in datas]
datas = '\n'.join(datas)
with open('res.txt', 'w', encoding='utf-8') as f:
    f.write(datas)

br.close()