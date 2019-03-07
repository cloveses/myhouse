from selenium import webdriver

br = webdriver.Firefox()

br.get('http://www.62665511.com/')
all_handles=br.window_handles
br.switch_to_window(all_handles[-1])
#选择重庆时时彩
br.find_element_by_xpath("//a[@id='countdown_lt_1']").click()
#选择第一位大
br.find_element_by_xpath("//input[@data-id='p1_da']").click()
#选择下注20
br.find_element_by_xpath("//a[@data-target='p1_da'][2]").click()
#确认
br.find_element_by_xpath("//a[@id='btn_order_confirm']").click()
#确认
br.find_element_by_xpath("//a[@id='order_ok']").click()
# 获取当前钱数
br.find_element_by_xpath("//div[@id='money_cash']/span").text