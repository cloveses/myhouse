import re
import time
from selenium import webdriver

# 启动火狐浏览器
br = webdriver.Firefox()
# 打开URL
br.get('http://ping.chinaz.com/www.baidu.com')
# 等待页面加载
br.implicitly_wait(60)
# 因页面中ajax完成时间长，加入以下判断等待
while True:
    cc = br.find_element_by_xpath("//ul/li[@class='item']")
    ds = re.findall(r'\d+', cc.text)
    # 判断页面中待ping资源数和完成数是否相等，相等则表示AJAX请求完成
    if ds and ds[0] == ds[-1]:
        break
    else:
        time.sleep(30)

#获取页面中的所有要获取的内容的div元素
containers = br.find_elements_by_xpath("//div[@id='speedlist']/div")
datas = []
for c in containers[1:]:
    #获取元素的文本内容
    datas.append(c.text.split('\n')[:-1])

for data in datas:
    print(data)

# 数据合并后写入文件
datas = [','.join(d) for d in datas]
datas = '\n'.join(datas)
with open('res.txt', 'w', encoding='utf-8') as f:
    f.write(datas)
    
# 关闭浏览器
br.close()