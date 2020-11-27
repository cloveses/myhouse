import xlrd
import sqlite3
import sys
import os

def get_file_datas(filename,row_deal_function=None,grid_end=0,start_row=1):
    """start_row＝1 有一行标题行；gred_end=1 末尾行不导入"""
    """row_del_function 为每行的数据类型处理函数，不传则对数据类型不作处理 """
    wb = xlrd.open_workbook(filename)
    ws = wb.sheets()[0]
    nrows = ws.nrows
    datas = []
    for i in range(start_row,nrows-grid_end):
        row = ws.row_values(i)
        # print(row)
        if row_deal_function:
            row = row_deal_function(row)
        datas.append(row)
    return datas


class MyDb:
    def __init__(self, filename):
        self.filename = filename
        self.cursor = self.get_dbcon()

    def get_dbcon(self):
        self.con = sqlite3.connect(self.filename)
        cursor = self.con.cursor()
        return cursor

    def create_table(self, sql):
        self.cursor.execute(sql)
        self.con.commit()

    def insert(self, create_sql, sql, datas):
        self.create_table(create_sql)
        self.cursor.executemany(sql, datas)
        self.con.commit()
        self.con.close()

def row_data_clean(row):
    return [str(r) for r in row]

if __name__ == '__main__':
    filename = 'my.db'
    xlsx_filename = input('源电子表格文件名：')
    if not xlsx_filename:
        xlsx_filename = 'my.xlsx'
    if not os.path.exists(xlsx_filename):
        print('你指定的文件不存在：', xlsx_filename)
        sys.exit(0)
    datas = get_file_datas(xlsx_filename, row_data_clean)
    mydb = MyDb(filename)
    tab_name = input('数据库中数据表的表名：')
    create_sql = input('创建表格的SQL列表和类型:\naa text,bb int...\n')
    create_sql = ' '.join(('create table', tab_name, '(', create_sql, ')'))
    # print('insert into tabname () vlaues()')
    sql_colname = input('插入数据表的列名:')
    sql_params = ','.join(['?' for i in range(len(datas[0]))])
    sql =' '.join(('insert into', tab_name, '(', sql_colname, ') values (', sql_params, ')'))
    # print(sql)
    mydb.insert(create_sql, sql, datas)