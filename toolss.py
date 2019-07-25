from selenium import webdriver
import xlrd
import time

def get_explorer(purl):
    br = webdriver.Firefox()
    br.get(purl)
    return br

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

def main(br, datas):
    br = get_explorer('https://xj.ahjygl.gov.cn/SMS.UI/Pages/Common/Login.aspx')
    # br.implicitly_wait(20)
    input('手工登录完成？')
    datas = get_file_datas('in.xlsx')
# def main():
    for data in datas:
        print(data)
        print(data[2], data[4], data[5])
        br.switch_to_frame('right')
        br.switch_to_frame('UpperHalf')
        id_html = br.find_element_by_xpath('//input[@id="ctl00_ContentPlaceHolder_TextBox_StudentIDNO"]')
        id_html.clear()
        id_html.send_keys(data[15])
        query_html = br.find_element_by_xpath('//input[@id="ctl00_ContentPlaceHolder_Button_Search"]')
        query_html.click()
        # query_html = br.find_element_by_xpath('//a[@id="ctl00_ContentPlaceHolder_GridView_StudentList_ctl02_linkButton_Result"]')
        # query_html.click()
        input('请点击查询与核查按钮')
        br.switch_to_default_content()
        br.switch_to_frame('right')
        br.switch_to_frame('LowerHalf')
        checker_html = br.find_element_by_xpath('//input[@id="ctl00_ContentPlaceHolder_TextBox_HCR"]')
        checker_html.send_keys(data[5])
        unit_html = br.find_element_by_xpath('//input[@id="ctl00_ContentPlaceHolder_TextBox_SZDW"]')
        unit_html.send_keys(data[6])
        phnumber_html = br.find_element_by_xpath('//input[@id="ctl00_ContentPlaceHolder_TextBox_SJHM"]')
        p = str(int(data[7])) if isinstance(data[7], float) else data[7]
        phnumber_html.send_keys(p)
        parent_html = br.find_element_by_xpath('//input[@id="ctl00_ContentPlaceHolder_TextBox_JZXM"]')
        parent_html.send_keys(data[8])
        gx_html = br.find_element_by_xpath('//input[@id="ctl00_ContentPlaceHolder_TextBox_YXSGX"]')
        gx_html.send_keys(data[9])
        gxph_html = br.find_element_by_xpath('//input[@id="ctl00_ContentPlaceHolder_TextBox_LXDH"]')
        p = str(int(data[10])) if isinstance(data[10], float) else data[10]
        if not p:
            p = '无'
        gxph_html.send_keys(p)
        memo_html = br.find_element_by_xpath('//input[@id="ctl00_ContentPlaceHolder_TextBox_HCQKSM"]')
        memo_html.send_keys(data[11])
        input('请选择类别后再点击保存和确认弹出的对话框。')
        br.switch_to_default_content()
        q = input('是否继续？(q为退出)')
        if q.lower() == 'q':
            break


if __name__ == '__main__':
    main()