from selenium import webdriver
import time

def get_explorer(purl):
    br = webdriver.Firefox()
    br.get(purl)
    return br

def main():
    br = get_explorer(url)
    br.implicitly_wait(20)
    input('手工登录完成？')
    element = br.find_element_by_xpath('')
    element.send_keys(data)
