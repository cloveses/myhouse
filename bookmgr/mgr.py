from model import *

@db_session
def register():
    # print('******welcome gto LibrarySystem ******')
    username = input("请输入用户名：")
    psd = input("请输入密码：")
    psd2 = input("请确认密码：")
    if (not username) or (not psd) or (not psd2):
        return '用户名和密码等输入项均不能为空！'

    if psd.isdigit() or psd.isalpha() or len(psd) < 6:
        return '密码最小6位，并包含字母和数字！'
        
    if not psd == psd2:
        return '确认密码不匹配！'
        
    if exists(u for u in UserDb if u.username==username):
        return '用户名已注册！'
        
    try:
        UserDb(username=username,password=psd)
        return True
    except:
        return '保存数据库失败！'


@db_session
def login(username, psd):
    if not username or not psd:
        return '用户名和密码均不能为空！'
    if select(u for u in UserDb if u.username==username and u.password==psd).first():
        return True
    else:
        return "登录失败,请重新登录"

@db_session
def changePassword(username, psd, psd2):
    if (not username) or (not psd) or (not psd2):
        return '用户名和密码等输入项均不能为空！'
    u = select(u for u in UserDb if u.username==username and u.password==psd).first()
    if u:
        u.password = psd2
        return True
    else:
        return '用户不存在或旧密码错误！'

@db_session
def selectAllbook():
    try:
        print('书名\t作者\t分类\t价格\t描述')
        for book in select(b for b in BookDb):
            print(book.bookname,book.author,book.category,book.price,book.desc)
        return 'success'
    except:
        return '失败！'

@db_session
def selectOneBookByName(bookname):
    book = select(b for b in BookDb if b.bookname==bookname).first()
    if book:
        return (book.bookname,book.author,book.category,str(book.price),book.desc)
    else:
        return '书籍不存在！'

@db_session
def selectBooksByPrice(minprice, maxprice):
    try:
        minprice = float(minprice)
        maxprice = float(maxprice)
    except:
        return '价格输入错误！'
    if maxprice <= minprice:
        return '价格范围错误！'
    books = select(b for b in BookDb if between(b.price, minprice, maxprice))
    if not books:
        return '书籍不存在！'
    else:
        return [(book.bookname,book.author,book.category,str(book.price),book.desc) for book in books]


@db_session
def addOneBook(params):
    try:
        params['price'] = float(params['price'])
    except:
        return '价格输入错误！'
    params = {k:v for k,v in params.items() if v}
    if len(params) < 5:
        return '书籍参数不足！'
    BookDb(**params)
    return True

@db_session
def modifyOneBookByName(bookname, author, price, category, desc):
    book = BookDb.get(bookname=bookname)
    if not book:
        return '书籍不存在！'
    try:
        price = float(price)
    except:
        return '价格输入错误！'
    book.author = author
    book.price = price
    book.category = category
    book.desc = desc
    return True

@db_session
def deleteOneBookByName(bookname):
    if not bookname:
        return '书名不能为空！'
    book = BookDb.get(bookname=bookname)
    if not book:
        return '书籍不存在！'
    book.delete()
    return True

@db_session
def exit():
    print('欢迎下次光临')
    return 'success'


def manageBook():

    """图书管理中心"""
    while True:

        print("************welcome to Book Manage Center*********")
        print("1: 查询所有书籍信息")
        print("2：通过书名查询一本书")
        print("3：通过价格查询书籍")
        print("4： 添加一本书")
        print("5： 删除一本书")
        print("6： 修改一本书")
        print("7: 退出系统")

        select = input()

        if select == '1':
            selectAllbook()

        elif select == '2':
            bookname = input('请输入书名：')
            ret = selectOneBookByName(bookname)
            if isinstance(ret, str):
                print(ret)
            else:
                print('书名\t作者\t分类\t价格\t描述')
                print('\t'.join(ret))

        elif select == '3':
            low = input("请输入最低价格：")
            high = input("请输入最高价格：")
            ret = selectBooksByPrice(low, high)
            if isinstance(ret, str):
                print(ret)
            else:
                print('书名\t作者\t分类\t价格\t描述')
                for book in ret:
                    print('\t'.join(book))

        elif select == '4':
            params = {}
            params['bookname'] = input("请输入书名：")
            params['author'] = input("请输入作者：")
            params['category'] = input("请输入分类：")
            params['price'] = input("请输入价格：")
            params['desc'] = input("请输入描述：")
            ret = addOneBook(params)
            if isinstance(ret, str):
                print(ret)
            elif ret:
                print('添加成功')
            else:
                print("添加失败")

        elif select == '5':
            bookname = input("请输入书名：")
            ret = deleteOneBookByName(bookname)
            if isinstance(ret, str):
                print(ret)
            elif ret:
                print('删除成功')
            else:
                print("删除失败")

        elif select == '6':
            bookname = input("请输入书名：")
            author = input("请输入作者：")
            category = input("请输入分类：")
            price = input("请输入价格：")
            desc = input("请输入描述：")
            ret = modifyOneBookByName(bookname, author, price, category, desc)
            if isinstance(ret, str):
                print(ret)
            elif ret:
                print('修改成功')
            else:
                print('修改失败')

        elif select == '7':
            ret = exit()
            break

        else:
            print('输入错误！')

def main():

    """主函数"""

    while True:
        print("************welcome to LibrarySystem*********")
        print("1:login    2: regist   3: changepass\n")
        select = input()

        if select == '1':
            username = input("请输入用户名：")
            psd = input("请输入密码：")
            ret = login(username, psd)
            if isinstance(ret, str):
                print(ret)
            elif ret:
                print('登录成功')
                manageBook()
                break
            else:
                print('登录失败')


        elif select == '2':
            ret = register()
            if isinstance(ret, str):
                print(ret)
                print('注册失败')
            elif ret:
                print('注册成功')
            else:
                print('注册失败')

        elif select == '3':
            username = input("请输入用户名：")
            psd = input("请输入密码：")
            psd2 = input("请输入新密码：")
            ret = changePassword(username, psd, psd2)
            if isinstance(ret, str):
                print(ret)
            elif ret:
                print('修改成功')
        else:
            print('输入错误！')

if __name__ == '__main__':
    main()