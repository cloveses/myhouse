from PIL import Image, ImageDraw, ImageFont

def get_datas(filename):
    # 打开文件
    with open(filename, 'r', encoding='utf-8-sig') as f:
        ds = []
        # 按行读取数据，并分行处理
        for line in f.readlines():
            # print(line)
            row = line.split(',')
            row = [r.strip() for r in row]
            if row[1].isdigit() and row[2].isdigit():
                print(row)
                # 对指定列进行数据类型转换为浮点数
                row[4] = float(row[4])
                row[6] = float(row[6])
                ds.append(row)
        # 按E列数据大小排序
        ds.sort(key=lambda x: x[4])
        # 获取E列小于G列的
        before_low_datas = [d for d in ds if d[4] < d[6]]
        # 获取E列大小G列的
        after_high_datas = [d for d in ds if d[4] > d[6]]
        res = []
        res.extend(before_low_datas)
        res.extend(after_high_datas)
        return res

def get_points(filename='point.txt'):
    res = {}
    with open(filename) as f:
        for line in f.readlines():
            if line.strip():
                # print(line.split(','))
                name, x, y = line.strip().split(',')
                res[name.lower()] = (int(x), int(y))
    return res

def write_image(imgfile, filename='raw_data.csv'):
    img = Image.open(imgfile)
    draw = ImageDraw.Draw(img)
    datas = get_datas(filename)
    points = get_points()
    font = ImageFont.truetype('C:/windows/fonts/Arial.ttf', size=14)
    for data in datas:
        name = data[0].lower()
        if name in points:
            draw.text(points[name], str(data[4]), font=font,  fill = (255,0,0))
    img.save('s.jpg')
    img.close()
    # print('dddd:',datas)
    for i in range(len(datas)):
        datas[i][4] = str(datas[i][4])
        datas[i][6] = str(datas[i][6])
    datas = [','.join(d) for d in datas]
    with open('res_data.csv', 'w') as f:
        f.write('\n'.join(datas))


if __name__ == '__main__':
    # print(get_datas('raw_data.csv'))
    # print(get_points())
    write_image('usa.jpg')
