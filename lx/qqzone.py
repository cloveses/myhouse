from selenium import webdriver
import time,random,requests

# br = webdriver.Firefox()
# br.get('https://user.qzone.qq.com/46420820/infocenter')
# time.sleep(5)
# br.switch_to_frame('login_frame')
# time.sleep(random.randint(2,6))
# br.find_element_by_id('switcher_plogin').click()

# time.sleep(random.randint(2,6))
# br.find_element_by_id('u').send_keys('46420820')
# time.sleep(random.randint(2,6))
# br.find_element_by_id('p').send_keys('87937339')
# time.sleep(random.randint(2,6))
# br.find_element_by_id('login_button').click()
# time.sleep(random.randint(2,6))
# br.switch_to_default_content()

# success = input('pause')

# br.find_element_by_xpath("//a[@title='日志']").click()
# time.sleep(random.randint(2,6))
# br.switch_to_frame('tblog')
# time.sleep(random.randint(2,6))
# log_urls = []

# while True:
#     time.sleep(random.randint(1,2))
#     logs = br.find_element_by_id('listArea').find_elements_by_tag_name('a')
#     for log in logs:
#         url = log.get_attribute('href')
#         if url.startswith('http'):
#             log_urls.append(url)
#     try:
#         br.find_element_by_partial_link_text('下一页').click()
#     except:
#         break

# log_urls = list(set(log_urls))
# with open('url.txt','w') as f:
#     for url in log_urls:
#         f.write(url)
#         f.write('\n')


import re

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

with open('url.txt','r') as f:
    log_urls = f.read()
log_urls = log_urls.split('\n')
log_urls = [u.strip() for u in log_urls if u.strip()]

br = webdriver.Firefox()

failed_urls = []

for index,url in enumerate(log_urls):
    time.sleep(random.randint(2,6))
    br.get(url)
    if index == 0:
        a = input('pause:')
    br.switch_to_frame('tblog')
    title = br.find_element_by_class_name('blog_tit_detail').text
    content_eles = br.find_element_by_id('blogDetailDiv')
    text = content_eles.text

    try:
        with open(validateTitle(title)+'.txt','w',encoding='utf-8') as f:
            f.write(text)
    except:
        print(url,'failed!')
        failed_urls.append(url)

    imgs = content_eles.find_elements_by_tag_name('img')
    for index,img in enumerate(imgs):
        time.sleep(random.randint(2,6))
        img_url = img.get_attribute('src')
        if img_url and img_url.startswith('http'):
            try:
                with open(''.join((validateTitle(title),'_',str(index),'.jpg')),'wb') as f:
                    f.write(requests.get(img_url).content)
            except:
                print('img failed!')
with open('failed_urls.txt', 'w',encoding='utf-8') as f:
    for u in failed_urls:
        f.write(url)
        f.write('\n')
