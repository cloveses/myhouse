from selenium import webdriver

br = webdriver.Firefox()

br.get('https://f6.com/')

br.find_element_by_xpath("//div[contains(@class,'logbtn')]/a").click()


br.find_element_by_xpath("//input[@id='login_username']").send_keys('baga0556')

br.find_element_by_xpath("//input[@id='login_pwd']").send_keys('zhangjie0556')

br.find_element_by_xpath("//input[@type='submit']").click()

br.find_element_by_xpath("//ul[@class='cf']//li[4]//a").click()


all_handles=br.window_handles
br.switch_to_window(all_handles[-1])
#选择重庆时时彩
br.find_element_by_xpath("//a[@id='countdown_lt_1']").click()
#选择第五位单
br.find_element_by_xpath("//input[@data-id='p5_dan']").click()
#选择下注20
br.find_element_by_xpath("//a[@data-target='p5_dan'][2]").click()
#确认
br.find_element_by_xpath("//a[@id='btn_order_confirm']").click()
#确认
br.find_element_by_xpath("//a[@id='order_ok']").click()
# 获取当前钱数
br.find_element_by_xpath("//div[@id='money_cash']/span").text


br.find_element_by_xpath("//div[@id='pan_status']").get_attribute('class')  #'close','open'
br.find_element_by_xpath("//div[@id='money_cash']/span").text #金额数