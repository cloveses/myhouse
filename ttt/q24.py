
# accounts = {'cid':[name,idcode,balance,[(date,type,amount,)]]}

import datetime
ID = 0

def deposit(accounts,cid,amount):
    if cid not in accounts:
        print('无此帐户，存款失败！')
        return
    accounts[cid][2] += amount
    accounts[cid][-1].append((datetime.datetime.now(),'deposit',amount))
    print('存款：%f 元' % amount, '余额：%f 元' % accounts[cid][2])

def draw(accounts,cid,amount):
    if amount > accounts[cid][2]:
        print('余额不足，取款失败！')
        return
    accounts[cid][2] -= amount
    accounts[cid][-1].append((datetime.datetime.now(),'draw',amount))
    print('取款：%f 元' % amount, '余额：%f 元' % accounts[cid][2])


def create(accounts,name,idcode):
    global ID
    cid = str(ID + 1)
    ID = ID + 1
    accounts[cid] = [name,idcode,0,[(datetime.datetime.now(),'create',0),]]

def cancel(accounts,cid):
    if cid in accounts:
        amount = accounts[cid][2]
        draw(accounts,cid,amount)
        del accounts[cid]
        print('销户成功！')
    else:
        print('无此帐户，销户失败！')

def query(accounts,cid):
    if cid in accounts:
        for h in accounts[cid][-1]:
            print(h)

def main():
    print('-----------')
    print('开户－－cr, 销户－－ca, 存款－－de, 取款－－dr, 查询历史--qu, 退出－－exit')
    accounts = {}
    while True:
        command = input('请输入命令：')
        if not command:
            continue
        if command.lower() == 'cr':
            name = input('客户姓名：')
            idcode = input('客户证件号：')
            if name and idcode:
                create(accounts,name,idcode)
            else:
                print('姓名和证件号都不能为空！')
        elif command.lower() == 'ca':
            cid = input('客户账号：')
            if cid:
                cancel(accounts,cid)
        elif command.lower() == 'qu':
            cid = input('客户账号：')
            if cid:
                query(accounts,cid)
        elif command.lower() == 'de':
            cid = input('客户账号：')
            amount = float(input('存款金额：'))
            if cid:
                deposit(accounts,cid,amount)
        elif command.lower() == 'dr':
            cid = input('客户账号：')
            amount = float(input('取款金额：'))
            if cid:
                draw(accounts,cid,amount)
        elif command.lower() == 'exit':
            break
        else:
            print('命令错误！')

if __name__ == '__main__':
    main()