from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import datetime
import sys
from lxml import etree

def log(info, name='log.txt'):
    with open(name, 'a', encoding='utf-8') as f:
        f.write(str(datetime.datetime.now()))
        f.write(' zhu:')
        f.write(info)
        f.write('\n')

def get_opened(html):
    datas = []
    html_parse = etree.HTML(html)
    for i in range(10):
        datas.extend(html_parse.xpath('//td[{}]/text()'.format(i+1)))
    datas = [int(i) % 2 for i in datas]
    return datas

def main(times=3):
    history_datas = []

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
    time.sleep(3)
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

    html = br.find_element_by_xpath("//table[@id='result_table_right']//tbody").get_attribute('innerHTML')
    history_datas = get_opened(html)

    # print('history_datas:', history_datas)

    print('init:', cash)
    order_status = 0
    # order_cashes = {0:'10', 1:'19.7', 2:'38.8'}
    order_cashes = {0:'1', 1:'2', 2:'4', 3:'8', 4:'15', 5:'30', 6:'59'}
    phase_directs = ["//input[@data-id='p1_dan']", "//input[@data-id='p1_shuang']"]
    phase_direct = 0

    while True:
        # 等待开盘
        while True:
            pan_status = br.find_element_by_xpath("//div[@id='pan_status']").get_attribute('class')
            if pan_status != 'open':
                time.sleep(60)
            else:
                break

        if cash == 0:
            break

        ratio = (len([i for i in history_datas if i==1]) / len(history_datas)) * 100

        if ratio - 56 > 0.000000000000000000001:
            phase_direct = 1
        else:
            phase_direct = 0

        if ratio - 60 > 0.000000000000000000000001:
            times = 4
        elif ratio - 65 > 0.000000000000000000000001:
            times = 6
        else:
            times = 3

        print('ratio:', ratio, 'phase_direct:', phase_direct, 'times:', times)

        if cash >= float(order_cashes[order_status]):
            br.find_element_by_xpath(phase_directs[phase_direct]).send_keys(order_cashes[order_status])
            log(order_cashes[order_status])
        else:
            br.find_element_by_xpath(phase_directs[phase_direct]).send_keys(str(cash))
            log(str(cash))

        #确认
        br.find_element_by_xpath("//a[@id='btn_order_confirm']").click()
        #确认
        time.sleep(5)
        br.find_element_by_xpath("//a[@id='order_ok']").click()

        # 投注完成后等待余额减少并更新当前剩现金数
        time.sleep(10)
        while True:
            cash_new = float(br.find_element_by_xpath("//div[@id='money_cash']/span").text )
            if abs(cash - cash_new) > 0.0000000000001:
                cash = cash_new
                # print('phase finished....', cash)
                break
            else:
                time.sleep(30)
        log('remain:' + str(cash))
        # print('remain:', cash)

        # 等待封盘
        while True:
            pan_status = br.find_element_by_xpath("//div[@id='pan_status']").get_attribute('class')
            if pan_status != 'close':
                time.sleep(30)
            else:
                # print('wait close...end.')
                break

        # 等待开奖 获取当前剩现金数
        while True:
            order_cash = int(br.find_element_by_xpath("//div[@id='curr_phase_sum']/span").text )
            if order_cash == 0:
                # print('phase update...finished.')
                break
            else:
                time.sleep(30)

        time.sleep(3)
        while True:
            result = br.find_element_by_xpath("//div[@id='phase_result_phase']").text
            # print(result, result.endswith('开奖结果'))
            if result.endswith('开奖结果'):
                cash_new = float(br.find_element_by_xpath("//div[@id='money_cash']/span").text )
                print('find result...finished')
                break
            else:
                time.sleep(120)

        # 更新投注状态
        if abs(cash_new - cash) > 0.00000000001:
            order_status = (order_status + 1) % times
            if phase_direct == 0:
                history_datas.append(1)
            else:
                history_datas.append(0)
        else:
            order_status = 0
            if phase_direct == 1:
                history_datas[0] += 1

            if phase_direct == 0:
                history_datas.append(0)
            else:
                history_datas.append(1)

        if len(history_datas) > 100:
            history_datas = history_datas[-100:]

        cash = cash_new
        print('remain:', cash)
        log('remain:' + str(cash))

if __name__ == '__main__':
    params = sys.argv
    if len(params) > 1:
        times = int(params[1])
        main(times)
    else:
        main()

