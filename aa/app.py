from flask import Flask, request, redirect, url_for, render_template, send_from_directory, abort
import os
from werkzeug.utils import secure_filename
import jieba
import csv
import fasttext as ff

app = Flask(__name__)

file_name=""

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':

        #上传训练数据并运行
        if 'train' in request.form:
            f=request.files['file']
            basepath=os.path.dirname(__file__)
            upload_path=os.path.join(basepath, 'static/uploads', secure_filename(f.filename))
            f.save(upload_path)
            train(f.filename)           #调用训练函数
            return redirect(url_for('upload'))
        #上传测试数据并运行
        elif 'test' in request.form:
            f=request.files['file_test']
            basepath=os.path.dirname(__file__)
            upload_path=os.path.join(basepath,'static/uploads',secure_filename(f.filename))
            f.save(upload_path)
            test(f.filename)            #调用测试函数
            return send_from_directory('static/uploads','result.csv',as_attachment=True)
    return render_template('upload.html')


# basefir="/home/sld/PycharmProjects/flask/static/uploads/"
basefir = os.path.dirname(__file__)
basefir = os.path.join(basefir,'static','uploads')
basefir = os.path.abspath(basefir)
print(basefir)
def prepare(filename):


    with open(os.path.join(basefir, filename)) as fr:            #读取上传文件
        text = csv.reader(fr)
        temp = next(text)
        text = list(text)
        list0 = []
        '''
        for row in text:
            name = str(row[0])
            seg = list(jieba.cut(name, cut_all=False))
            temp = 1
            for r in list0:
                if row[2] == r[0]:
                    for row_name in seg:
                        r[1].append(row_name)
                    temp = 0
                    break
            if temp == 1:
                list0.append([row[2], seg])
        '''
        for row in text:
            name=str(row[0])
            seg=list(jieba.cut(name,cut_all=False))
            list0.append([row[2],seg])
    return list0

def train(filename):
    list0=prepare(filename)
    ftrain = open(os.path.join(basefir, "new_train.txt"), "w")
    for row in list0:
        ftrain.write("__label__" + row[0])
        for tmp in row[1]:
            ftrain.write(" " + tmp)
        ftrain.write("\n")
    ftrain.close()
    # print('aaaaa')
    # os.system("/home/sld/fastText-0.1.0/fasttext supervised -input " + basefir + "new_train.txt -output " + basefir + "model") 
    classifier = ff.supervised(os.path.join(basefir, "new_train.txt"), os.path.join(basefir, "model")) #train_
    # classifier.save_model(os.path.join(basefir, "model.bin"))


def test(filename):
    with open (os.path.join(basefir, filename)) as fr:
        text = csv.reader(fr)
        temp = next(text)
        text = list(text)
        list0 = []
        ftest=open(os.path.join(basefir, "new_test.txt"),"w")
        for row in text:
            name=str(row[0])
            seg=list(jieba.cut(name,cut_all=False))
            ftest.write("__label__105")
            for r in seg:
                ftest.write(" "+r)
            ftest.write("\n")
        ftest.close()
    # result=os.popen("/home/sld/fastText-0.1.0/fasttext predict "+basefir+"model.bin "+basefir+"new_test.txt 5")
    # #result=os.popen("/home/sld/fastText-0.1.0/fasttext test "+basefir+"model.bin "+basefir+"cooking.v 5")
    classifier = ff.load_model(os.path.join(basefir, "model.bin"), label_prefix='__label__')
    result = classifier.predict(os.path.join(basefir, "new_test.txt"))
    result=list(result)
    '''
    with open (basefir+filename) as fr:
        text=csv.reader(fr)
        temp=next(text)
        text=list(text)
    '''
    list1=["商品名称","商品编码1","商品编码2","商品编码3","商品编码4","商品编码5"]
    out=open(basefir+"result.csv","w",newline="")
    csv_write=csv.writer(out,dialect="excel")
    csv_write.writerow(list1)
    bit=0
    for row in text:
        row_w=[row[0]]
        for num in range(0,5):
            print(result)
            row_w.append(result[bit][9+13*num:12+13*num])
        csv_write.writerow(row_w)
        bit=bit+1


if __name__ == '__main__':
    app.run()
