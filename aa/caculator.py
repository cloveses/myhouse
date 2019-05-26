#!/usr/bin/python
# -*- coding: UTF-8 -*-
from tkinter import *
C9=['C','/','X','<',7,8,9,'-',4,5,6,'+',1,2,3,'%','M',0,'.','=']
class app:
lists = []
lists1 = []
isPressSign = False
isPressNum = False
def __init__(self,master):
result = StringVar()
result.set(0)
self.result = result
result2 = StringVar()
result2.set('')
self.result2 = result2
label = Label(master,textvariable = result)
label.grid(row=0,column=0,columnspan=4,sticky = E)
label2 = Label(master,textvariable = result2)
label2.grid(row=1,column=0,columnspan=4,sticky = E)
button0 = Button(text=C9[0],width =2,height =1,command = lambda:self.pressCompute('C')).grid(row=2,column=0)
button1 = Button(text=C9[1],width =2,height =1,command = lambda:self.pressCompute('/')).grid(row=2,column=1)
button2 = Button(text=C9[2],width =2,height =1,command = lambda:self.pressCompute('*')).grid(row=2,column=2)
button3 = Button(text=C9[3],width =2,height =1,command = lambda:self.pressCompute('<')).grid(row=2,column=3)
button4 = Button(text=C9[4],width =2,height =1,command = lambda:self.pressNum('7')).grid(row=3,column=0)
button5 = Button(text=C9[5],width =2,height =1,command = lambda:self.pressNum('8')).grid(row=3,column=1)
button6 = Button(text=C9[6],width =2,height =1,command = lambda:self.pressNum('9')).grid(row=3,column=2)
button7 = Button(text=C9[7],width =2,height =1,command = lambda:self.pressCompute('-')).grid(row=3,column=3)
button8 = Button(text=C9[8],width =2,height =1,command = lambda:self.pressNum('4')).grid(row=4,column=0)
button9 = Button(text=C9[9],width =2,height =1,command = lambda:self.pressNum('5')).grid(row=4,column=1)
button10 = Button(text=C9[10],width =2,height =1,command = lambda:self.pressNum('6')).grid(row=4,column=2)
button11 = Button(text=C9[11],width =2,height =1,command = lambda:self.pressCompute('+')).grid(row=4,column=3)
button12 = Button(text=C9[12],width =2,height =1,command = lambda:self.pressNum('1')).grid(row=5,column=0)
button13 = Button(text=C9[13],width =2,height =1,command = lambda:self.pressNum('2')).grid(row=5,column=1)
button14 = Button(text=C9[14],width =2,height =1,command = lambda:self.pressNum('3')).grid(row=5,column=2)
button15 = Button(text=C9[15],width =2,height =1,command = lambda:self.pressCompute('%')).grid(row=5,column=3)
# button16 = Button(text=C9[16],command = lambda:self.pressNum('M')).grid(row=6,column=0)
button17 = Button(text=C9[17],width =2,height =1,command = lambda:self.pressNum('0')).grid(row=6,column=1)
button18 = Button(text=C9[18],width =2,height =1,command = lambda:self.pressCompute('.')).grid(row=6,column=0)
button19 = Button(text=C9[19],width =8,height =1,command = lambda:self.pressEqual()).grid(row=6,column=2,columnspan=2)


def pressNum(self,num):
if app.isPressSign == False:
pass
else:
# self.result.set(0)
app.isPressSign = False
oldnum = self.result.get()
if oldnum == '0':
self.result.set(num)
else:
newnum = oldnum+num
self.result.set(newnum)


def pressCompute(self,sign):
num = self.result.get()
app.lists1.append(num)
app.lists1.append(sign)
newnum = num+sign
app.isPressSign = True

if sign == 'C':
app.lists1[:]=[]
self.result.set(0)
self.result2.set(0)
elif sign == '<':
a = num[0:-1]
app.lists1[:]=[]
self.result.set(a)
else:
self.result.set(newnum)




def pressEqual(self):
curnum = self.result.get()
app.lists.append(curnum)


computrStr = ''.join(app.lists)
endNum = eval(computrStr)
self.result.set(endNum)
self.result2.set(computrStr)
app.lists[:]=[]







root=Tk()
display = app(root)
root.mainloop()