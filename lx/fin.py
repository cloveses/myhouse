import time
import numpy as np
import pandas as pd
import urllib.request


def getHtml(url):

    while True:

        try:
            html = urllib.request.urlopen(url, timeout=5).read()
            break
        except:
            print("超时重试")

    html = html.decode('gbk')
    return html


def get_stock(股票代码,分钟='15',长度='10',显示=0):

    yyy = time.time()
    day = '日期时间'
    open = '开盘价'
    high = '最高价'
    low = '最低价'
    close = '收盘价'
    volume = '成交量'
    数据 = pd.DataFrame(eval(getHtml('http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol='+股票代码+'&scale='+分钟+'&ma=no&datalen='+长度)))
    数据['股票代码'] = 股票代码.upper()
    数据 = 数据[['股票代码','日期时间', '开盘价', '最高价', '最低价', '收盘价', '成交量']]
    数据.iloc[:, 2:] = np.float32(数据.iloc[:, 2:])
    uuu = time.time()
    if 显示==0 :

        return 数据

    else:

        print(uuu - yyy)
        return 数据

def main():
    import time
    print(time.time())
    pdframes = []
    for code in np.load('fcode.npy'):
        data = get_stock(code)
        pdframes.append(data)
    print(time.time())
    return pdframes

if __name__ == '__main__':

    # 股票数据 = get_stock('sh600600', 分钟='15', 长度='10', 显示=0)
    # print(股票数据)
    # print([0])
    main()