
import pickle
import os
import datetime

class Product:

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount
        self.date = datetime.datetime.now()


class Category:

    def __init__(self,name):
        self.name = name
        self.purchases = []
        self.sellores = []
        self.product_amount = {}

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
            return
        self.sellores.append(Product(name,amount))
        self.product_amount -= amount

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


def main():
    products = {}
    if os.path.exists('q29.db'):
        with open('q29.db', 'rb') as f:
            products = pickle.load(f)

    print('-------------------')
    print('添加产品－－add')
    print('产品入库－－store')
    while True:
        command = input('请输入命令：')
        if not command:
            continue
        if command.lower() == 'add':
            add(products)
        elif command.lower() == 'store':
            store(products)
        # elif command.lower() == 'del':
        #     del_book(products)
        # elif command.lower() == 'search':
        #     search(products)
        # elif command.lower() == 'display':
        #     display(products)
        elif command.lower() == 'exit':
            with open('q29.db','wb') as f:
                pickle.dump(products,f)
            break
        else:
            print('命令错误！')

if __name__ == '__main__':
    main()