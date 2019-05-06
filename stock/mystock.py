class BaseInfo:

    def __init__(self, shost, sport):
        self.shost = shost
        self.sport = sport
        self.infos = {0:0, 1:0}

    def get_client(self):
        try:
            self.clientHq = TradeX.TdxHq_Connect(self.shost, self.sport)
        except TradeX.TdxHq_error as err:
            print ("error: ", err)
            self.clientHq = None

    def get_infos(self):
        if not self.clientHq:
            print('没有连接到服务器！')
        else:
            for market in self.infos.keys:
                
