# {姓名:{NUMBER:'', QQ:'', EMAIL:'', CITY:'', CODE:''},......}
# 要安装 pypinyin 库： pip install pypinyin
import pickle, os
import pypinyin

def add(books):
    musts = ('姓名', '手机号')
    params = {'姓名':'','手机号':'','QQ号':'','EMAIL':'', '城市':'', '邮编':''}
    for key in params.keys():
        params[key] = input(key+':')

    for must in musts:
        if must not in params:
            print(must, '不能为空！')
            return

    name = params['姓名']
    del params['姓名']
    books[name] = params

def edit(books):
    params = {'手机号':'','QQ号':'','EMAIL':'', '城市':'', '邮编':''}
    name = input('被修改联系人的姓名：')
    if not name or name not in books:
        print('姓名不能为空，或通讯录中不存在！')
        return
    for key in params.keys():
        params[key] = input(key+':')
    params = {k:v for k,v in params.items() if v}
    for k,v in params.items():
        books[name][k] = v
    print(books[name])
    print('修改成功!')

def del_book(books):
    name = input('被修改联系人的姓名：')
    if not name or name not in books:
        print('姓名不能为空，或通讯录中不存在！')
        return
    del books[name]
    print('成功删除!')


def search(books):
    print('按姓名搜？y')
    reply = input()
    if reply.lower() == 'y':
        name = input('被修改联系人的姓名：')
        if not name or name not in books:
            print('姓名不能为空，或通讯录中不存在！')
            return
        else:
            print(books[name])
    print('按手机号搜？y')
    reply = input()
    if reply.lower() == 'y':
        number = input('被修改联系人的姓名：')
        if not number:
            print('你输入空字符，查找失败！')
            return
        else:
            for k,v in books.items():
                if number in list(v.values()):
                    print(k,books[k])

def display(books):
    keys = list(books.keys())
    keys_p = [pypinyin.pinyin(k) for k in keys]
    keys_pp = []
    for ks in keys_p:
        temp = []
        for kp in ks:
            temp.extend(kp)
        keys_pp.append(''.join(temp))
    # print(keys_pp)
    keys = [(a,b) for a,b in zip(keys,keys_pp)]
    keys.sort(key=lambda s:s[1])
    keys = [k[0] for k in keys]
    for key in keys:
        print(key,books[key])


def main():
    books = {}
    if os.path.exists('q28.db'):
        with open('q28.db', 'rb') as f:
            books = pickle.load(f)

    print('-----------')
    print('添加联系人－－add')
    print('查找联系人－－search')
    print('编辑联系人－－edit')
    print('查找联系人－－del')
    print('显示联系人－－display')

    while True:
        command = input('请输入命令：')
        if not command:
            continue
        if command.lower() == 'add':
            add(books)
        elif command.lower() == 'edit':
            edit(books)
        elif command.lower() == 'del':
            del_book(books)
        elif command.lower() == 'search':
            search(books)
        elif command.lower() == 'display':
            display(books)
        elif command.lower() == 'exit':
            with open('q28.db','wb') as f:
                pickle.dump(books,f)
            break
        else:
            print('命令错误！')

if __name__ == '__main__':
    main()