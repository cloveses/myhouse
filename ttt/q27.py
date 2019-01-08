#以表格的形式存储，元素（man,woman,colnum）
#相邻行colnum-1为父子关系
import os
import pickle

def add_man(datas, father, man):
    if not father:
        datas.append([man,None,0])
    if not datas:
        datas.append([man,None,0])
    else:
        findex,colnum = -1,-1
        for index,data in enumerate(datas):
            if data[0] == father:
                findex = index
                colnum = data[-1]
        if findex == -1:
            print('无此父节点！')
            return
        for insertpos in range(findex+1,len(datas)):
            if datas[insertpos][-1] < colnum:
                break
        datas.insert(insertpos-1,(man,None,colnum+1))

def add_woman(datas,man,woman):
    for data in datas:
        if data[0] == man:
            data[1] = woman

def get_curr(datas, man):
    ind = -1
    colnum = -1
    for index,data in enumerate(datas):
        if data[0] = man:
            ind = index
            colnum = data[-1]
            break
    if ind != -1:
        return ind,colnum

def del_couple(datas, man):
    ind = -1
    for index,data in enumerate(datas):
        if data[0] == man:
            ind = index
            break
    if index != -1:
        del datas[index]

def query_father(datas, man):
    res = get_curr(datas,man)
    if res:
        ind,colnum = res
        indx = -1
        for index in range(ind-1,-1,-1):
            if datas[index][-1] == colnum - 1:
                indx = index
                break
        if indx != -1:
            print(datas[indx][0], datas[indx][1])

def query_brother(datas, man):
    res = get_curr(datas,man)
    if res:
        ind,colnum = res
        for index in range(ind-1,-1,-1):
            if datas[index][-1] < colnum:
                break
            if datas[index][-1] == colnum:
                print(datas[index][0])
        for data in datas[ind+1:]:
            if data[-1] < colnum:
                break
            if datas[-1] == colnum:
                print(data[0])
def query_child(datas, man):
    res = get_curr(datas, man)
    if res:
        ind,colnum = res
        for data in datas[ind+1:]:
            if data[-1] <=  colnum:
                break
            if data[-1] == colnum + 1:
                print(data[0])

def display(datas):
    for data in datas:
        print('/t' * data[-1])
        print(data[0],end=' ')
        if data[1]:
            print(data[1])

def main():
    datas = []
    if os.path.exists('q27.db'):
        with open('q27.db','rb') as f:
            datas = pickle.load(f)

    print('家谱系统')
    print('-------------------')
    print('添加儿子－－am, 添加媳妇－－aw, 删除－－dc')
    print('查询双亲－－qf, 查询兄弟－－qb, 查询孩子－－qc')
    print('树形输出－－q, 退出系统－－exit')

    while True:
        command = input('请输入命令：')
        if not command:
            continue
        if command == 'am':
            father = input('父亲姓名：')
            son = input('孩子姓名：')
            add_man(datas, father, son)
        elif command = 'aw':
            man = input('丈夫姓名：')
            woman = input('媳妇姓名：')
            add_woman(datas,man,woman)
        elif command = 'dc':
            man = input('姓名：')
            del_couple(datas, man)
        elif command == 'qf':
            father = input('父亲姓名：')
            query_father(datas, father)
        elif command == 'qb':
            man = input('姓名：')
            query_brother(datas,man)
        elif command == 'qc':
            man = input('父亲姓名：')
            query_child(datas, man)
        elif command == 'q':
            display(datas)
        elif command == 'exit':
            break

    with open('q27.db','wb') as f:
        pickle.dump(datas,f)

if __name__ == '__main__':
    main()

