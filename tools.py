import xlrd
import win32clipboard as w
import win32con

def get_clip():
    w.OpenClipboard()
    txt = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return txt

def set_clip(data):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardText(data)
    w.CloseClipboard()

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
        datas.append(row)
    return datas

def find_data(idcode, datas):
    for data in datas:
        if data[2].lower() == idcode.lower():
            return data

if __name__ == '__main__':
    filename = input('please input filename:')
    datas = get_file_datas(filename)
    while True:
        command = input(' q ? ')
        if command == 'q':
            break

        idcode = get_clip()
        if not idcode:
            print('Do not find idcode from clip!')
            continue
        else:
            data = find_data(idcode)
            if data:
                data = [str(int(d)) if isinstance(d, float) else str(d) for d in data]
                for d in data[:]:
                    c = None
                    set_clip(d)
                    c = input()
                    if c == 'q':
                        break
            else:
                print('Do not find idcode from excel!')
