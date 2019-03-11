from selenium import webdriver
import time

def main():
    br = webdriver.Firefox()

    br.get('https://f6.com/')
    time.sleep(1)
    br.find_element_by_xpath("//div[contains(@class,'logbtn')]/a").click()
    time.sleep(1)
    br.find_element_by_xpath("//input[@id='login_username']").send_keys('baga0556')
    br.find_element_by_xpath("//input[@id='login_pwd']").send_keys('zhangjie0556')
    time.sleep(1)
    br.find_element_by_xpath("//input[@type='submit']").click()
    time.sleep(1)
    br.find_element_by_xpath("//ul[@class='cf']//li[4]//a").click()
    time.sleep(5)
    all_handles=br.window_handles
    br.switch_to_window(all_handles[-1])
    #选择重庆时时彩
    br.find_element_by_xpath("//a[@id='countdown_lt_1']").click()
    time.sleep(2)
    cash = float(br.find_element_by_xpath("//div[@id='money_cash']/span").text )#金额数
    order_status = 0
    # order_cash = {0:'10', 1:'19.7', 2:'38.8'}
    order_cash = {0:'1', 1:'1.97', 2:'3.88'}

    pan_status = ''
    while pan_status != 'open':
        time.sleep(120)
        pan_status = br.find_element_by_xpath("//div[@id='pan_status']").get_attribute('class')

    while True:
        if cash == 0:
            break
        if cash >= order_cash[order_status]:
            br.find_element_by_xpath("//input[@data-id='p5_dan']").send_keys(order_cash[order_status])
        else:
            br.find_element_by_xpath("//input[@data-id='p5_dan']").send_keys(str(cash))
        #确认
        br.find_element_by_xpath("//a[@id='btn_order_confirm']").click()
        #确认
        br.find_element_by_xpath("//a[@id='order_ok']").click()

        pan_status = ''
        while pan_status != 'close':
            time.sleep(120)
            pan_status = br.find_element_by_xpath("//div[@id='pan_status']").get_attribute('class')

        pan_status = ''
        while pan_status != 'open':
            time.sleep(120)
            pan_status = br.find_element_by_xpath("//div[@id='pan_status']").get_attribute('class')

        cash_new = float(br.find_element_by_xpath("//div[@id='money_cash']/span").text )
        if cash_new > cash:
            order_status = (order_status + 1) % 3
        else:
            order_status = 0
        cash = cash_new

if __name__ == '__main__':
    main()