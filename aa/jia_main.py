from win32com import client as wc
import xlsxwriter

def save_datas_xlsx(filename,datas):
    #将一张表的信息写入电子表格中XLSX文件格式
    w = xlsxwriter.Workbook(filename)
    w_sheet = w.add_worksheet('sheet1')
    for rowi,row in enumerate(datas):
        for coli,celld in enumerate(row):
            w_sheet.write(rowi,coli,celld)
    w.close()

seqs = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10,'廿':20}

def get_seq(s):
    if len(s) == 1:
        return seqs[s]
    else:
        return seqs[s[0]] + seqs[s[1]]

all_datas = []
word = wc.Dispatch('Word.Application')
doc = word.Documents.Open('d:/lx/myhouse/aa/十一世张方成（联玉）一支36（已校）.doc',Encoding='gbk')
data = []
for index in range(2,len(doc.Paragraphs)):
    line = doc.Paragraphs[index].Range.text.strip()
    if line:
        line = line.replace('  ','k')
        res = [line[:3].replace('k','').strip(),line[4:7].replace('k','').strip(),line[8:].replace('k','').strip()]
        res = [r.replace(' ','') for r in res]
        if '世' in res[0]:
            if data:
                all_datas.append(data[:])
            data = []
            data.extend(res)
        else:
            data.extend(res)

    # if index >=50:
    #     break

for d in all_datas:
    d.insert(0,get_seq((d[0][:-1])))

all_datas.sort(key=lambda x:x[0])
for d in all_datas:
    if 3 < len(d) <= 7 and ('生子' in d[-1] or '生女' in d[-1]):
        d.insert(0,1)
    elif len(d) > 7 and ('生子' in d[-1] or '生女' in d[-1] or '生子' in d[-4] or '生女' in d[-4]):
        d.insert(0,1)
    else:
        d.insert(0,0)

preids = []
for d in all_datas:
    for index,ad in enumerate(all_datas):
        if d[4][:2] in ad[3]:
            preids.append(index)
            break
    else:
        preids.append(0)

wdatas = [['id', 'name', 'isnext', 'text', 'preId', 'ids', 'wife', 'daishu'],]
for index,(preid,d) in enumerate(zip(preids,all_datas),1):
    # print(preid,d)
    row = [index,d[3],d[0] if d[0] else '', d[4], preid+1, d[1], ''.join(d[5:]) if len(d) > 4 else '' , d[2]]
    wdatas.append(row[:])

# for wd in wdatas:
#     print(wd)

save_datas_xlsx('res.xlsx', wdatas)
