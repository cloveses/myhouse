import xlrd,xlwt

filename = 'a.xls'

def get_data():
    datas = []
    w = xlrd.open_workbook(filename)
    ws = w.sheets()[0]
    nrows = ws.nrows
    for i in range(nrows):
        data = ws.row_values(i)
        datas.append(data)
    #    print(datas)
    colnames,datas = datas[0],datas[1:]
    for i in range(len(datas)):
        datas[i][0] = int(datas[i][0])
    return colnames,datas

colnames,datas = get_data()


def add(row_data):
    row_data = row_data.split(',')
    # row_data[2] = int(row_data[2])
    seq = len(datas)
    data = [seq+1,]
    data.extend(row_data)
    datas.append(data)

def edit(seq,colname,data):
    datas[seq][colnames.index(colname)] = data

def query():
    for data in datas:
        print(data)

def del_data(seq):
    del datas[seq-1]

def save_datas():
    #将一张表的信息写入电子表格中
    #文件内容不能太大，否则输出文件会出错。
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('sheet1')
    for rowi,row in enumerate(datas):
        rr = ws.row(rowi)
        for coli,celld in enumerate(row):
            if isinstance(celld,int) or isinstance(celld,float):
                rr.set_cell_number(coli,celld)
            else:
                rr.set_cell_text(coli,celld)
    #rr = ws.row(4)
    w.save(filename)

def main():
    print('commands:add,edi,que,del,exit')
    while True:
        op = input('Pleas input a command:')
        if op == 'add':
            row_data = input('Please input data:')
            add(row_data)
        elif op == 'edi':
            seq = input('序号:')
            colname = input('列名：')
            data = input('数据：')
            if seq and colname and data and seq.isdigit() and colname in colnames and int(seq) < len(datas):
                edit(int(seq)-1, colname, data)
        elif op == 'que':
            query()
        elif op == 'del':
            seq = input('序号：')
            if seq and seq.isdigit():
                del_data(int(seq))
        elif op == 'exit':
            save_datas()
            break
        else:
            continue

if __name__ == '__main__':
    main()
