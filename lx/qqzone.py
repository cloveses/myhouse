from selenium import webdriver
import time

br = webdriver.Firefox()
br.get('https://user.qzone.qq.com/181564186/infocenter')
time.sleep(5)
br.switch_to_frame('login_frame')
br.find_element_by_id('switcher_plogin').click()
br.find_element_by_id('u').send_keys('181564186')
time.sleep(2)
br.find_element_by_id('p').send_keys('21jingxiang57')
time.sleep(2)
br.find_element_by_id('login_button').click()

time.sleep(3)
br.switch_to_default_content()
br.find_element_by_xpath("//a[@title='日志']").click()
time.sleep(2)
print(br.find_element_by_id('list_area').text)