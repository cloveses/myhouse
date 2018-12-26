import xlrd,xlwt

filename = 'a.xlsx'

def get_data():
     #既可以打开xls类型的文件，也可以打开xlsx类型的文件
    #w = xlrd.open_workbook('text.xls')
    #w = xlrd.open_workbook('acs.xlsx')
    datas = []
    w = xlrd.open_workbook(filename)
    ws = w.sheets()[0]
    nrows = ws.nrows
    for i in range(nrows):
        data = ws.row_values(i)
        datas.append(data)
    #    print(datas)
    return datas

datas = get_data()
colnames,datas = datas[0],datas[1:]


def add(row_data):
    datas.append(row_data)

def edit(seq,colname,data):
    ws,wb = get_ws()
    for row in ws.iter_rows():
        if row[0].value == seq:
            row[datas[0].index(colname)].value = data
            break
    wb.save(filename)
    datas = load()

def query(colname,data):
    datas = load()
    index = datas[0].index(colname)
    for data in datas:
        if data[index] == data:
            print(data)

def del_data(seq):
    ws,wb = get_ws()
    for row in ws.iter_rows():
        if row[0].value == seq:
            row[-1].value = '已售空'
    wb.save(filename)
    datas = load()

def main():
    print('commands:add,edi,que,del')
    while True:
        op = input('Pleas input a command:')
        if op == 'add':
            row_data = input('Please input data:')
            row_data = row_data.split(',')
            row_data[0] = int(row_data[0])
            row_data[3] = int(row_data[3])
        elif op == 'edi':
            edit_data = input('data:')
            edit_data = edit_data.split(',')
            edit(*edit_data)
        elif op == 'que':
            datass = input('data:')
            datass = datass.split(',')
            query(*datass)
        elif op == 'del':
            datass = input('Please input seq:')
            datass = int(datass)
            del_data(datass)
        elif op == 'exit':
            break
        else:
            continue

if __name__ == '__main__':
    # main()
    add((2,'aaa','bbb',30,'ccc'))
