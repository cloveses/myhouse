import sqlite3
conn = sqlite3.connect('e:\\film.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE base(电影名称 TEXT,放映厅 TEXT,票价 INTEGER);''')
while True:
    id = input('请输入电影名称:')
    if id == '0':
        break
    number = input('请输入放映厅序号:')
    price = input('请输入票价:')
    SQL='''insert into base(电影名称,放映厅,票价)values('%s','%s','%s');'''%(id,number,price)
    print(SQL)
    cur.execute(SQL)
    conn.commit()
conn.close()
