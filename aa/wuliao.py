import requests
import xlrd
import xlsxwriter
import urllib.parse
from lxml import etree
import time
import random

def save_datas_xlsx(filename,datas):
    w = xlsxwriter.Workbook(filename)
    w_sheet = w.add_worksheet('sheet1')
    for rowi,row in enumerate(datas):
        for coli,celld in enumerate(row):
            w_sheet.write(rowi,coli,celld)
    w.close()

def get_file_datas(filename,row_deal_function=None,grid_end=0,start_row=1):
    """start_row＝1 有一行标题行；gred_end=1 末尾行不导入"""
    """row_del_function 为每行的数据类型处理函数，不传则对数据类型不作处理 """
    wb = xlrd.open_workbook(filename)
    ws = wb.sheets()[0]
    nrows = ws.nrows
    datas = []
    for i in range(start_row,nrows-grid_end):
        row = ws.row_values(i)
        print(row)
        datas.append(row)
    return datas

datas  = get_file_datas('mdndata.xlsx')
# print(datas)

sess = requests.Session()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept':'text/html;q=0.9,*/*;q=0.8',
        'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding':'gzip',
        'Connection':'close',
        'Referer':'http://www.baidu.com/link?url=_andhfsjjjKRgEWkj7i9cFmYYGsisrnm2A-TN3XZDQXxvGsM9k9ZZSnikW2Yds4s&wd=&eqid=c3435a7d00006bd600000003582bfd1f'
        }

sess = requests.Session()
sess.get('https://www.findchips.com/',headers=headers)

for mpn in datas:
    time.sleep(random.randint(1,4))
    mpn = 'GRM21BR61A225KA01L'
    r = sess.get('https://www.findchips.com/search/' + urllib.parse.quote(mpn))
    r.encoding = 'utf-8'

html_tree = etree.HTML(r.text)
tbodies = html_tree.xpath('//tbody')

prices = []
for tbody in tbodies:
    price = tbody.xpath('.//td//ul//li//span/text()')
    prices.append(price)

print(prices)

manufacters = html_tree.xpath('//h3[@class="distributor-title"]//a/text()')
manufacters = [m.strip() for m in manufacters]
manufacters = [m for m in manufacters if m]
print(len(prices),len(manufacters))
res_datas = {}
for price, manufacter in zip(prices, manufacters):
    if price and price[1].startswith('$'):
        res_datas[manufacter] = price

print(res_datas)

    break