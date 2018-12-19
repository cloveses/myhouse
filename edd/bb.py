# -*- coding:utf-8 -*-
#
import tkinter
import functools
from tkinter.simpledialog import askstring

VIPS = ('34353','3333')
texts = [('汉堡包：12元',12), ('蛋挞：7元',7), ('猪肉卷：10元',10), ('饮料：5元',5)]

def make_checks(root):
    check_vars = []
    for text,price in texts:
        c = tkinter.IntVar()
        c.set(0)
        check_vars.append(c)
        check = tkinter.Checkbutton(root,
            text=text, variable=c,
            onvalue=price, offvalue=0)
        check.pack()
    return check_vars

def get_price(check_vars, label):
    res = [c.get() for c in check_vars]
    txt = ','.join([t[0] for t,r in zip(texts,res) if r])
    txt = '你点了' + txt + ',共'

    price = sum(res)
    r = askstring('会员付款界面',    # 创建字符串输入对话框
            '请输入会员码：',                         # 指定提示字符
            initialvalue='tkinter')                 # 指定初始化文本
    if r and r in VIPS:
        discount_price = price * 0.8
        label['text'] = txt + '%d元。' % price + '折扣价为%.2f元。' % discount_price
    else:
        label['text'] = txt + '%d元。' % price


root = tkinter.Tk()
root.title('自助点餐')
label= tkinter.Label(root, text="你好，请问需要什么？")
label.pack()

check_vars = make_checks(root)
labela = tkinter.Label(root, text=' ')
labela.pack()

ok_btn = tkinter.Button(root, text='OK', command=functools.partial(get_price, check_vars, labela))
ok_btn.pack()
root.mainloop()         
