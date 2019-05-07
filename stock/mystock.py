import math
import TradeX

class Base:

    def __init__(self, shost, sport):
        self.shost = shost
        self.sport = sport

    def get_client(self):
        try:
            self.clientHq = TradeX.TdxHq_Connect(self.shost, self.sport)
        except TradeX.TdxHq_error as err:
            print ("error: ", err)
            self.clientHq = None


class BaseInfo(Base):

    def __init__(self, shost, sport, market):
        super().__init__(shost, sport)
        self.market = market

    def get_infos(self):
        self.get_client()
        if not self.clientHq:
            print('没有连接到服务器！')
        else:
            errinfo, count = self.clientHq.GetSecurityCount(self.market)
            if errinfo != '':
                print(errinfo)
                self.stocks = None
            else:
                self.stocks = count

    def get_stocklist(self):
        self.get_infos()
        self.stocks_lst = []
        if self.stocks:
            for start in range(math.ceil(self.stocks/1000)):
                errinfo, count, result = self.clientHq.GetSecurityList(self.market, start * 1000)
                if errinfo:
                    print(errinfo)
                else:
                    result = result.split('\n')
                    result = [r.split('\t') for r in result]
                    result = [[r[0],r[2],r[5]] for r in result if r[0].isdigit()]
                    self.stocks_lst.extend(result)

            if self.stocks_lst:
                for i in range(math.ceil(self.stocks/80)):
                    start = i*80
                    end = (i+1)*80
                    current_stocks = [(self.market, stock[0]) for stock in self.stocks_lst[start:end]]
                    errinfo, count, result = self.clientHq.GetSecurityQuotes(current_stocks)
                    if errinfo:
                        print(errinfo)
                    else:
                        result = result.split('\n')
                        result = [r.split('\t') for r in result]
                        result = [r[3:5] for r in result if r[1].isdigit()]
                        for index,stock in enumerate(self.stocks_lst[start:end]):
                            stock.extend(result[index])


if __name__ == '__main__':
    bi = BaseInfo('124.160.88.183', 7709, 0)
    bi.get_stocklist()
    # print(bi.stocks_lst[:8])
    codes = ['00000'+str(i) for i in range(1,10)]
    for i in bi.stocks_lst:
        if i[0] in codes:
            print(i)