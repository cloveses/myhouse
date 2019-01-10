# {'categoryname':Category,....}
# p

import pickle
import os
import datetime

class Product:

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount
        self.store = amount
        self.date = datetime.datetime.now()


class Category:

    def __init__(self,name):
        self.name = name
        self.histories = [] # 入库历史产品列表
        self.purchases = [] # 入库产品列表
        self.sellores = []  # 出库产品列表
        self.product_amount = {} # 产品数量 {'name':amount}

    def purchase(self,name,amount):
        self.purchases.append(Product(name,amount))
        if name in self.product_amount:
            self.product_amount[name] += amount
        else:
            self.product_amount[name] = amount

    def sell(self,name,amount):
        if name not in self.product_amount:
            print('无此产品！')
            return
        if self.product_amount[name] < amount:
            print('产品库存不足！', self.product_amount[name])
            print('现将产品全部出库！')
            amount = self.product_amount[name]

        self.sellores.append(Product(name,amount)) # 记录出库记录
        self.product_amount[name] -= amount
        if self.product_amount[name] < 10:
            print(name, '目前库存量为：', self.product_amount[name], '达到或低于预警线！')
        # 对库存列表中产品作出库处理，减去库存量，出完的就进入历史列表
        sells = []
        for p in self.purchases:
            if p.name == name:
                if p.store == amount:
                    sells.append(p)
                    p.store = 0
                    break
                elif p.store > amount:
                    p.store -= amount
                    break
                else:
                    amount -= p.store
                    p.store = 0
                    sells.append(p)
        if sells:
            for p in sells:
                self.histories.append(p)
                self.purchases.remove(p)

    def display(self,name):
        print(name, '库存列表：')
        for p in self.purchases:
            if p.name == name:
                print('入库日期：',p.date,'库存数：',p.store)
        print(name,'出库信息：')
        for p in self.sellores:
            if p.name == name:
                print('出库日期：',p.date,'出库数：',p.amount)
        print('总库存量：',self.product_amount[name])

def add(products):
    category = input('请输入产品类别名称：')
    if not category:
        print('产品类别名称不能为空！')
        return
    elif category in products:
        print('产品类别已存在！')
        return
    else:
        products[category] = Category(category)

def store(products):
    category = input('请输入产品类别名称：')
    if not category or category not in products:
        print('产品类别名称不能为空或不存在的类别！')
        return
    cate = products[category]
    name,amount = input('请输入产品名称：'),input('请输入产品数量：')
    if not name or not amount.isdigit():
        print('产品类别名称不能为空，或产品数量输入不正确！')
        return
    cate.purchase(name,int(amount))

def sell(products):
    category = input('请输入产品类别名称：')
    if not category or category not in products:
        print('产品类别名称不能为空或不存在的类别！')
        return
    cate = products[category]
    name,amount = input('请输入产品名称：'),input('请输入产品数量：')
    if not name or not amount.isdigit():
        print('产品类别名称不能为空，或产品数量输入不正确！')
        return
    amount = float(amount)
    if name not in cate.product_amount:
        print('库中无此产品！')
        return
    if cate.product_amount[name] < amount:
        print('库存不足，当前剩余：',cate.product_amount[name])
        print('现将产品全部出库！')
        amount = cate.product_amount[name]
    cate.sell(name, amount)

def display(products):
    category = input('请输入产品类别名称：')
    if not category or category not in products:
        print('产品类别名称不能为空或不存在的类别！')
        return
    cate = products[category]
    name = input('请输入产品名称：')
    if not name or name not in cate.product_amount:
        print('库中无此产品或无库存了！')
        return
    cate.display(name)

def main():
    products = {}
    if os.path.exists('q29.db'):
        with open('q29.db', 'rb') as f:
            products = pickle.load(f)

    print('-------------------')
    print('添加产品类别－－add')
    print('产品入库－－store')
    print('产品出库－－sell')
    print('产品显示－－display')
    print('退出系统－－exit')
    while True:
        command = input('请输入命令：')
        if not command:
            continue
        if command.lower() == 'add':
            add(products)
        elif command.lower() == 'store':
            store(products)
        elif command.lower() == 'sell':
            sell(products)
        elif command.lower() == 'display':
            display(products)
        elif command.lower() == 'exit':
            with open('q29.db','wb') as f:
                pickle.dump(products,f)
            break
        else:
            print('命令错误！')

if __name__ == '__main__':
    main()