import requests
import xlrd
import xlsxwriter
import urllib.parse
from lxml import etree
import time
import random
from datetime import datetime
import sys

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
        # print(row)
        datas.append(row)
    return datas

MANUFACTERS = ['Digi-key', 'Mouser Electronics', 'TTI', 'Verical', 'Arrow Electronics',
    'Future Electronics' , 'Avnet', 'Rochestor', 'element14 Asia-Pacific', 'RS Components']

def need_manufacter(manu):
    for m in MANUFACTERS:
        if manu.lower() in m.lower() or manu.lower() == m.lower():
            return True

datas  = get_file_datas('testmdn.xlsx')
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
try:
    sess.get('https://www.findchips.com/',headers=headers, timeout=(30,60))
except:
    print('网络访问异常，请重新运行。')
    sys.exit(0)
# print('get 1')

all_datas = []
for mpn in datas:
    time.sleep(random.randint(1,2))
    need = abs(int(mpn[3]))
    mpn = mpn[1]
    print(mpn)
    # mpn = 'GRM21BR61A225KA01L'
    try:
        r = sess.get('https://www.findchips.com/search/' + urllib.parse.quote(mpn) + '?currency=USD', timeout=(30,60))
    except:
        # print('Error:',mpn)
        all_datas.append(['Error',] * 4)
        continue
    # print('get 2')
    r.encoding = 'utf-8'

    html_tree = etree.HTML(r.text)
    manu_divs = html_tree.xpath('//div[@class="distributor-results"]')
    results = {}

    for manu_div in manu_divs:
        manufacter = ''.join(manu_div.xpath('.//h3//a/text()')).strip()
        if not manufacter:
            manufacter = ''.join(manu_div.xpath('.//h3/text()')).strip()
        # print('manufacter:', manufacter)
        trs = manu_div.xpath('.//tbody//tr')
        tr_datas = []
        for tr in trs:
            stock = tr.xpath('.//td[@class="td-stock"]/text()')
            # print('stock:', stock)
            if isinstance(stock, list):
                stock = ''.join(stock)
            stock = [s for s in stock if s.isdigit()]
            if stock:
                stock = int(''.join(stock))
            else:
                stock = 0
            if stock:
                prices = tr.xpath('.//td//ul//li//span/text()')
                # print('prices:', prices)
                if prices:
                    prices = [[int(total),float(price[1:].replace(',', ''))] for total,price in zip(prices[::2],prices[1::2])]
                    prices.sort(key=lambda x:x[0], reverse=True)
                    tr_datas.append([stock,prices])
        # print(manufacter)
        if tr_datas:
            results[manufacter] = tr_datas
    # print(results)
    results = {k:v for k,v in results.items() if need_manufacter(k)}

    a_results = []
    for manufacter, cates in results.items():
        for cate in cates:
            if cate[0] >= need:
                for apply_num, price in cate[1]:
                    if apply_num <= need:
                        a_results.append([manufacter,apply_num,price,cate[0]])
                        break

    if a_results:                    
        a_results.sort(key=lambda x: x[-2])
        # print(a_results)
        res = a_results[0]
    else:
        # print(results)
        for manufacter, cates in results.items():
            for cate in cates:
                for apply_num, price in cate[1]:
                    if apply_num <= cate[0]:
                        a_results.append([manufacter,cate[0],apply_num,price])
                        break

        a_results.sort(key=lambda x:x[-2], reverse=True)
        # print(a_results)
        res = []
        start = 0
        i = 0
        # print(a_results)
        while start <= need and i < len(a_results):
            res.append([a_results[i][0],a_results[i][2],a_results[i][3], a_results[i][1]])
            start += a_results[i][1]
            i += 1

    if res and isinstance(res[0],list):
        ms = [m[0] for m in res]
        apply_num = [str(m[1]) for m in res]
        price = [str(m[-2]) for m in res]
        stocks = [str(m[-1]) for m in res]
        res = [','.join(ms), ','.join(apply_num), ','.join(price), ','.join(stocks)]
    elif res:
        res = [str(r) for r in res]
    else:
        res = ['0',] * 4

    all_datas.append(res)

data = [['Part', 'MPN','MFG', 'Need qty','Spot buy QTY', 'Price', 'Stock', 'Supplier', 'total_stocks'],]
for d, all_data in zip(datas, all_datas):
    nd = d[:]
    nd.extend(all_data[1:])
    nd.append(all_data[0])
    if ',' in nd[-2]:
        nd.append(sum([int(s) for s in nd[-2].split(',')]))
    else:
        nd.append(int(nd[-2]) if nd[-2].isdigit() else '')
    data.append(nd)

filename = datetime.now().isoformat()
filename = filename[:filename.index('.')].replace(':','') + '.xlsx'
save_datas_xlsx(filename, data)

