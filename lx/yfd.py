from selenium import webdriver
import time,random,requests
import re
br = webdriver.Firefox()
br.get('http://ufang.51jt.com/ufang')
br.find_element_by_id('username').send_keys('13252223300')
br.find_element_by_id('password').send_keys('111111')
br.find_elements_by_css_selector('input[type=submit]')[0].click()
br.switch_to_frame('jerichotabiframe_0')

br.find_elements_by_tag_name('td')[0].text

# 全选
br.find_elements_by_css_selector('input[class=allchoose]')[0].click()

#批量购买
br.find_elements_by_tag_name('button')[-1].click()
#确认对话框操作
w=br.switch_to_alert()
w.accept()