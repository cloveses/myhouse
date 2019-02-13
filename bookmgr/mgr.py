from model import *

@db_session
def register():
    # print('******welcome gto LibrarySystem ******')
    username = input("请输入用户名：")
    psd = input("请输入密码：")
    psd2 = input("请确认密码：")
    if (not username) or (not psd) or (not psd2):
        return '用户名和密码等输入项均不能为空！'
        
    if not psd == psd2:
        return '确认密码不匹配！'
        
    if exists(u for u in UserDb if username==username):
        return '用户名已注册！'
    try:
        UserDb(username=username,password=psd)
        return True
    except:
        return '保存数据库失败！'


@db_session
def login(username, psd):
    # username = input("请输入用户名：")
    # psd = input("请输入密码：")
    if not username or not psd:
        return '用户名和密码均不能为空！'
    if select(u for u in UserDb if username==username and password=psd).first():
        return True
    else:
        return "登录失败,请重新登录"

@db_session
def changePassword(uid, psd, psd2):
    # username = input("请输入用户名：")
    # psd = input("请输入密码：")
    # psd2 = input("请输入新密码：")
    if (not username) or (not psd) or (not psd2):
        return '用户名和密码等输入项均不能为空！'
    if not psd == psd2:
        return '确认密码不匹配！'
    u = select(u for u in UserDb if username==username and password=psd).first()
    if u:
        u.password = psd2
        return True
    else:
        return '用户不存在或旧密码错误！'

@db_session
def selectAllbook():
    try:
        for book in BookDb.select():
            print('书名\t作者\t分类\t价格\t描述')
            print(book.bookname,book.author,book.category,book.price,book.desc,book.publish_date)
        return 'success'
    except:
        return '失败！'

@db_session
def selectOneBookByName(bookname):
    book = select(b for b in BookDb if b.bookname==bookname).first()
    if book:
        return book.to_dict()
    else:
        return '书籍不存在！'

@db_session
def selectBooksByPrice(minprice, maxprice):
    if maxprice <= minprice:
        return '价格范围错误！'
    books = select(b for b in BookDb if between(b.price, minprice, maxprice))
    if not books:
        return '书籍不存在！'
    else:
        return [(book.bookname,book.author,book.category,book.price,book.desc,book.publish_date) for book in books]

