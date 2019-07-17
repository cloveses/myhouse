class Company:
    companyList = []
    companyNum = 0

    def __init__(self, name, intro):
        self.companyName = name
        self.intro = intro
        self.employee_list = []
        self.cost = 0
        self.profit = 0
        self.sales_volume = 0
        Company.companyList.append(name)
        Company.companyNum += 1

    def get_companyNum(cls):
        return cls.companyNum

    def get_comanyList(cls):
        return cls.companyList


    def recruit(self, name, age, cost=10000, *infos):
        info = [name,age]
        info.extend(infos)
        self.employee_list.append(info)
        self.cost += cost

    def dismiss(self, name, cost=5000):
        for employee in self.employee_list:
            if employee[0] == name:
                break
        self.employee_list.remove(employee)
        self.cost += cost

    def adPromotion(self, cost):
        self.cost += cost

    def payInsurance(self, fee=1000):
        self.cost += len(self.employee_list) * fee

    def payTax(self, fee=500):
        self.cost += fee * len(self.employee_list)

    def sale(self, quality, price, profit_per=0.5):
        self.sales_volume += quality * price
        self.profit += quality * price * profit_per

    def getEmployeeList(self):
        return self.employee_list

    def getProfit(self):
        return self.profit





if __name__ == '__main__':

    #功能验证
    c0 = Company('阿里巴巴','供求信息平台')
    c0.recruit('alex',18, cost=20000)
    c0.recruit('Eric',20, cost=10000)
    print('{}公司员工详细信息列表:{}'.format(c0.companyName,c0.getEmployeeList()))

    c0.dismiss('Eric')

    c0.adPromotion(5000)
    c0.payInsurance()
    c0.payTax()
    c0.sale(50,100)
    print('{}公司员工详细信息列表:{}'.format(c0.companyName,c0.getEmployeeList()))
    print('{}公司当前利润：{}'.format(c0.companyName,c0.getProfit()))

    c1 = Company('百度','搜索引擎')
    c1.recruit('liyanhong',30, cost=50000)
    c1.recruit('likaifu',50, cost=40000)
    print('{}公司员工详细信息列表:{}'.format(c1.companyName,c1.getEmployeeList()))

    print('公司名列表：',Company.companyList)
    print('公司总个数：',Company.companyNum)