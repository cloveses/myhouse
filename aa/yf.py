import os

def exit():
    print("退出系统")#退出系统

def main():
    print("-"*40)
    print("     学生管理系统V1.0     ")
    print("1.创建文件夹")
    print("2.改变文件存储路径")
    print("3.读取学生名单")
    print("4.创建学生详细信息存储文本")
    print("5.增加学生详细信息")
    print("6.增加学生属性")
    print("7.查询所有学生信息")
    print("8.查询单个学生信息")
    print("9.修改学生信息")
    print("0.退出系统")
    print("-"*42)
    selects = [exit, make_dir, save_path, stud_lst, txt_to,
            stud_info, get_attribute, query, ad_stud, edit]
    select = int(input("请输入要选择的功能序号:"))
    if select >= 0 and select < len(selects):
        selects[select]()
    else:
        error()


#1 创建文件夹功能
def make_dir():
    name = input("请输入您要创建的文件夹名：")
    
    if not os.path.exists(name):
        os.mkdir(name)
        print("创建成功")
        repeat()
    else:
        print("文件名已经存在！")
        repeat()

# 2 改变文件存储路径功能
def save_path():
    name = input("请输入您要修改的文件夹名：")
    list = os.listdir('./')
    if name in list:
        str = os.path.abspath(name)
        print("您要修改的文件夹现在位置：",str)
        str = input("请输入您要修改到的路径：")
        os.chdir(str)
        print("执行成功")
        repeat2()
    else:
        print("不存在此文件夹")
        repeat2()

# 3 读取学生名单功能
def stud_lst():
    strp = "E:/untitled/.idea"
    file = open("C:/untitled/.idea/学生名单.txt", 'r')
    strlist = file.readlines()
    print("学生名单：")
    print(strlist)
    file.close()
    repeat3()
#4.创建学生信息存储文本
def txt_to():
    liststr=os.listdir('./')
    print("文件夹下的所有文件")
    for i in liststr:
        print(i)
    str1=input("请输入您想要打开的文件夹:")
    if i in  liststr:
        path1='./'+str1
        os.chdir(path1)
        n=int(input("请输入学生人数:"))
        for i in range(n):
            strstu=input("请输入学生姓名：:")
            filename=strstu+'.txt'
            stu=open(filename,'w')
            id=input ("请输入学号：:")
            idstr="sno:"+id+"\n"
            namestr="student's name:"+strstu+'\n'
            grade=input("请输入学生班级:")
            gradestr="student's grade:"+grade+'\n'
            stu.write(idstr)
            stu.write(namestr)
            stu.write(gradestr)
            stu.close()
            stu=open(filename,'r')
            print(stu.read())
            stu.close()
            repeat4()
    else:
        print("there wasn't flie in here")
        repeat4()
#5 增加学生详细信息功能:
def stud_info():
    strp="C:/untitled/.idea"
    file=open("C:/untitled/.idea/学生名单.txt",'r')
    strlist=file.readlines()
    lenght=len(strlist)
    print(strlist)
    for i in range(lenght):
        str1=strlist[i]
        str=strp+str1[:-1]+"学生信息.txt"
        print(str)
        filestu=open(str,'a')
        print("%s的家乡:"%(str1[:-1]))
        strinput="的家乡："+input("")+'\n'
        filestu.write(strinput)
        print("%s的评价"%(str1[:-1]))
        strinput="评价："+input("")+'\n'
        filestu.write(strinput)
        filestu.write("专业：软件技术\n")
        filestu.close()
        file.close()
    repeat5()
#6 增加学生属性功能
def get_attribute():
    strp = "C:/untitled/.idea"
    file = open("C:/untitled/.idea/学生名单.txt")
    strlist = file.readlines()
    lenght = len(strlist)
    print(strlist)
    for i in range(lenght):
        str1 = strlist[i]
        str = strp + str1[:-1] + "学生信息.txt"
        print(str)
        filestu = open(str, 'w')
        str2 = '姓名:' + str1
        filestu.write(str2)
        print("%s的爱好" % (str1[:-1]))
        strinput = "爱好:" + input("") + '\n'
        filestu.write(strinput)
        print("%s的成绩" % (str1[:-1]))
        strinput = "成绩：" + input("") + '\n'
        filestu.write(strinput)
        filestu.close()

    file.close()
    repeat6()
    
#7 查询所有学生信息功能
def query():
    import os
    str = os.getcwd()
    print(str)
    os.chdir("C:/untitled")
    str = os.getcwd()
    print(str)
    list = os.listdir()
    print("所有学生信息如下：")
    print(list)
    '''index=1
    while (index<len(list)):
        file=open(len(list),'r')
        l=file.readlines()
        print(l)
        index+=1
        file.close()*/'''
    repeat7()
#8 查询单个学生信息功能
#9 修改学生信息功能
def ad_stud():
    import os
    str = os.getcwd()
    print(str)
    os.chdir("C:/untitled")
    str = os.getcwd()
    print(str)
    list = os.listdir('./')
    print(list)
    list1 = input("请输入你要查看的学生：")
    if list1 in list:
        print(list1)
        file = open(list1, 'r')
        str2 = file.readlines()
        print(str2)
        file.close()
        repeat9()
    else:
        print("没有这个学生信息")
        repeat9()
#10 退出系统
def edit():
    import os
    str = os.getcwd()
    print(str)
    os.chdir("C:/untitled")
    str = os.getcwd()
    print(str)
    list = os.listdir()
    print(list)
    stufind = input("您要查找的学生：")
    if stufind in list:
        stu = open(stufind, 'r')
        listxinxi = stu.readlines()
        for j in listxinxi:
            print(j[:-1])
        print("s" * 30)
        stu.close()
        stuo = open(stufind, 'w')
        update = input("您要修改的信息")
        updatav = input("值")
        for t in listxinxi:
            print(t[0:2])
            if update == t[:2]:
                t = update + ":" + updatav + '\n'
            stuo.write(t)
        stuo.close()
        stu = open(stufind, 'r')
        listxinxi = stu.readlines()
        for j in listxinxi:
            print(j[:-1])
        print("s" * 30)
        stu.close
    else:
        print("错了")
    repeat10()


def fanhui():
     key= input("确定要退出吗？（Yes Or No,keepiing）")
     if  key == "Yes":
         print("结束运行")
     elif  key == "fh":
         main()
     elif  key=="继续":
        main()
     else:
         error()
def error():
    print("输入有误，请重新输入！")
    key = input("返回上一层，结束,继续:")
    if key == "结束":
        print("结束运行")
    elif key == "fh":
        main()
    elif key == "继续":
       create()
    else:
        fh()
def repeat():
    key = input("返回上一层，结束,继续:")
    if key == "结束":
        print("结束运行")
    elif key == "fh":
        main()
    elif key == "继续":
       make_dir()
    else:
        fh()
def repeat2():
    key = input("返回上一层，结束,继续:")
    if key == "结束":
        print("结束运行")
    elif key == "fh":
        main()
    elif key == "继续":
       save_path()
    else:
        fh()
def repeat3():
    key = input("返回上一层，结束,继续:")
    if key == "结束":
        print("结束运行")
    elif key == "fh":
        main()
    elif key == "继续":
       stud_lst ()
    else:
        fh()
def repeat4():
    key = input("返回上一层，结束,继续:")
    if key == "结束":
        print("结束运行")
    elif key == "fh":
        main()
    elif key == "继续":
       txt_to ()
    else:
        fh()
def repeat5():
    key = input("返回上一层，结束,继续（:")
    if key == "over":
        print("结束运行")
    elif key == "fh":
        main()
    elif key == "继续":
       stud_info()
    else:
        fh()

def repeat6():
    key = input("返回上一层，结束,继续:")
    if key == "结束":
        print("结束运行")
    elif key == "fh":
        main()
    elif key == "继续":
       get_attribute ()
    else:
        fh()

def repeat7():
    key = input("返回上一层，结束,继续:")
    if key == "结束":
        print("结束运行")
    elif key == "fh":
        main()
    elif key == "继续":
       query ()
    else:
        fh()
def repeat9():
    key = input("返回上一层，结束,继续:")
    if key == "结束":
        print("结束运行")
    elif key == "fh":
        main()
    elif key == "继续":
       ad_stud ()
    else:
        fh()

def repeat10():
    key = input("返回上一层，结束,继续:")
    if key == "结束":
        print("结束运行")
    elif key == "fh":
        main()
    elif key == "继续":
       edit ()
    else:
        fh()
main()
