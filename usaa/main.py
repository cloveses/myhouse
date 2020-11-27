import xlrd
import openpyxl

# 定义按行读取电子表格文件中的数据，并返回
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
    # 存放男性有关数据
    male_datas = []
    # 存取女性有关数据
    female_datas = []
    for i,data in enumerate(datas):
        # 当出现男性数据行时，连续读7行数据
        if data[0] == 'MALE':
            for index in range(i+1, i+8):
                male_datas.extend([datas[index][4], datas[index][5], round(datas[index][4]/datas[index][2], 1),
                datas[index][10], datas[index][11], round(datas[index][10]/datas[index][2], 1)])
        # 当出现女性数据行时，连续读7行数据
        if data[0] == 'FEMALE':
            for index in range(i+1, i+8):
                female_datas.extend([datas[index][4], datas[index][5], round(datas[index][4]/datas[index][2], 1),
                datas[index][10], datas[index][11], round(datas[index][10]/datas[index][2], 1)])
    # 返回结果
    return male_datas, female_datas

# 定义写数据到电子表格文件的函数
def save2file(filename, srcfilename):
    # 调用函数，获取源数据
    datas = get_file_datas(srcfilename)
    # 调用函数对数据进行处理
    mdatas, fdatas = clear(datas)
    # 打开数据表格并写入
    wb = openpyxl.load_workbook(filename)
    sheet = wb.get_sheet_by_name("Sheet1")
    for i, d in enumerate(mdatas):
        sheet['C%d' % (i+2)] = d
    for i, d in enumerate(fdatas):
        sheet['D%d' % (i+2)] = d
    # 保存文件
    wb.save(filename)


if __name__ == '__main__':
    # datas = get_file_datas('table01.xlsx')
    # print(datas[7][0])
    # print(datas[8][0])
    save2file('工作簿2.xlsx', 'table01.xlsx')
