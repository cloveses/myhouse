import xlrd
import openpyxl

def get_file_datas(filename,row_deal_function=None,grid_end=0,start_row=0):
    """start_row＝1 有一行标题行；gred_end=1 末尾行不导入"""
    """row_del_function 为每行的数据类型处理函数，不传则对数据类型不作处理 """
    wb = xlrd.open_workbook(filename)
    ws = wb.sheets()[0]
    nrows = ws.nrows
    datas = []
    for i in range(start_row,nrows-grid_end):
        row = ws.row_values(i)
        # print(row)
        datas.append(row)
    return datas

def clear(datas):
    male_datas = []
    female_datas = []
    for i,data in enumerate(datas):
        if data[0] == 'MALE':
            for index in range(i+1, i+8):
                male_datas.extend([datas[index][4], datas[index][5], round(datas[index][4]/datas[index][2], 1),
                datas[index][10], datas[index][11], round(datas[index][10]/datas[index][2], 1)])
        if data[0] == 'FEMALE':
            for index in range(i+1, i+8):
                female_datas.extend([datas[index][4], datas[index][5], round(datas[index][4]/datas[index][2], 1),
                datas[index][10], datas[index][11], round(datas[index][10]/datas[index][2], 1)])
    return male_datas, female_datas

def save2file(filename, srcfilename):
    datas = get_file_datas(srcfilename)
    mdatas, fdatas = clear(datas)
    wb = openpyxl.load_workbook(filename)
    sheet = wb.get_sheet_by_name("Sheet1")
    for i, d in enumerate(mdatas):
        sheet['C%d' % (i+2)] = d
    for i, d in enumerate(fdatas):
        sheet['D%d' % (i+2)] = d
    wb.save(filename)


if __name__ == '__main__':
    # datas = get_file_datas('table01.xlsx')
    # print(datas[7][0])
    # print(datas[8][0])
    save2file('工作簿2.xlsx', 'table01.xlsx')
