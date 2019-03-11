from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import datetime

def log(info, name='log.txt'):
    with open(name, 'a', encoding='utf-8') as f:
        f.write(str(datetime.datetime.now()))
        f.write(' zhu:')
        f.write(info)
        f.write('\n')

def main():
    br = webdriver.Firefox()

    br.get('https://f6.com/')
    time.sleep(1)
    br.find_element_by_xpath("//div[contains(@class,'logbtn')]/a").click()
    time.sleep(1)
    name = input('name:').strip()
    br.find_element_by_xpath("//input[@id='login_username']").send_keys('baga' + name)
    pw = input('pw:').strip()
    br.find_element_by_xpath("//input[@id='login_pwd']").send_keys('zhangjie' + pw)
    time.sleep(1)
    br.find_element_by_xpath("//input[@type='submit']").click()
    time.sleep(43)
    input('Continue ...')
    element = br.find_element_by_xpath("//ul[@class='cf']//li[4]//a")
    ActionChains(br).move_to_element(element)
    time.sleep(3)
    br.find_element_by_xpath("//ul[@class='cf']//li[4]//a").click()
    input('Continue ...')
    time.sleep(5)
    all_handles=br.window_handles
    br.switch_to_window(all_handles[-1])
    #选择重庆时时彩
    br.find_element_by_xpath("//a[@id='countdown_lt_1']").click()
    time.sleep(2)
    cash = float(br.find_element_by_xpath("//div[@id='money_cash']/span").text )#金额数
    print('init:', cash)
    order_status = 0
    # order_cash = {0:'10', 1:'19.7', 2:'38.8'}
    order_cash = {0:'1', 1:'1.97', 2:'3.88'}

    # 等待开盘
    while True:
        pan_status = br.find_element_by_xpath("//div[@id='pan_status']").get_attribute('class')
        if pan_status != 'open':
            time.sleep(60)
        else:
            break

    while True:
        if cash == 0:
            break
        if cash >= float(order_cash[order_status]):
            br.find_element_by_xpath("//input[@data-id='p5_dan']").send_keys(order_cash[order_status])
            log(order_cash[order_status])
        else:
            br.find_element_by_xpath("//input[@data-id='p5_dan']").send_keys(str(cash))
            log(str(cash))
        #确认
        br.find_element_by_xpath("//a[@id='btn_order_confirm']").click()
        #确认
        br.find_element_by_xpath("//a[@id='order_ok']").click()

        # 投注完成后等待余额减少并更新当前剩现金数
        time.sleep(30)
        while True:
            cash_new = float(br.find_element_by_xpath("//div[@id='money_cash']/span").text )
            if abs(cash - cash_new) > 0.0000000000001:
                cash = cash_new
                break
            else:
                time.sleep(60)
        log('remain:' + str(cash))
        print('remain:', cash)

        # 等待开盘
        while True:
            pan_status = br.find_element_by_xpath("//div[@id='pan_status']").get_attribute('class')
            if pan_status != 'open':
                time.sleep(120)
            else:
                break

        # 等待开奖后获取当前剩现金数
        time.sleep(30)
        while True:
            cash_new = float(br.find_element_by_xpath("//div[@id='money_cash']/span").text )
            if abs(cash - cash_new) > 0.0000000000001:
                break
            else:
                time.sleep(120)

        # 更新投注状态
        if cash_new > cash:
            order_status = (order_status + 1) % 3
        else:
            order_status = 0
        cash = cash_new
        print('remain:', cash)
        log('remain:' + str(cash))

if __name__ == '__main__':
    main()