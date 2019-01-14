# {姓名:{NUMBER:'', QQ:'', EMAIL:'', CITY:'', CODE:''},......}
# 要安装 pypinyin 库： pip install pypinyin
import pickle, os
import pypinyin

# 新增通讯录
def add(books):
    musts = ('姓名', '手机号')
    params = {'姓名':'','手机号':'','QQ号':'','EMAIL':'', '城市':'', '邮编':''}
    # 输入每个信息项
    for key in params.keys():
        params[key] = input(key+':')
    # 检查必须项是否为空
    for must in musts:
        if must not in params:
            print(must, '不能为空！')
            return

    name = params['姓名']
    del params['姓名']
    books[name] = params

# 编辑通讯录（根据姓名）
def edit(books):
    params = {'手机号':'','QQ号':'','EMAIL':'', '城市':'', '邮编':''}
    name = input('被修改联系人的姓名：')
    if not name or name not in books:
        print('姓名不能为空，或通讯录中不存在！')
        return
    # 逐项逐项输入
    for key in params.keys():
        params[key] = input(key+':')
    # 去除输入为空的项
    params = {k:v for k,v in params.items() if v}
    for k,v in params.items():
        books[name][k] = v
    print(books[name])
    print('修改成功!')

# 删除通联系人（根据联系人姓名）
def del_book(books):
    name = input('被修改联系人的姓名：')
    if not name or name not in books:
        print('姓名不能为空，或通讯录中不存在！')
        return
    del books[name]
    print('成功删除!')

# 搜索通讯录
def search(books):
    print('按姓名搜？y')
    reply = input()
    if reply.lower() == 'y':
        name = input('被修改联系人的姓名：')
        # 接受联系人姓名，查找并删除
        if not name or name not in books:
            print('姓名不能为空，或通讯录中不存在！')
            return
        else:
            print(books[name])
    # 按输入的手机号搜索通讯录
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

# 显示通讯录
def display(books):
    # 获取姓名，并转换为拼音后排序
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
    # 依据排序的姓名从通讯录中获取并输入
    keys = [k[0] for k in keys]
    for key in keys:
        print(key,books[key])


def main():
    books = {}
    # 数据文件存在则读取
    if os.path.exists('q28.db'):
        with open('q28.db', 'rb') as f:
            books = pickle.load(f)

    print('-----------')
    print('添加联系人－－add')
    print('查找联系人－－search')
    print('编辑联系人－－edit')
    print('查找联系人－－del')
    print('显示联系人－－display')
    # 命令循环，依据输入命令执行相关功能
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
            # 退出时保存通讯录
            with open('q28.db','wb') as f:
                pickle.dump(books,f)
            break
        else:
            print('命令错误！')

if __name__ == '__main__':
    main()