from PIL import Image, ImageDraw, ImageFont

def get_datas(filename):
    with open(filename, 'r', encoding='utf-8-sig') as f:
        ds = []
        for line in f.readlines():
            # print(line)
            row = line.split(',')
            row = [r.strip() for r in row]
            if row[1].isdigit() and row[2].isdigit():
                print(row)
                row[4] = float(row[4])
                row[6] = float(row[6])
                ds.append(row)
        ds.sort(key=lambda x: x[4])
        before_low_datas = [d for d in ds if d[4] < d[6]]
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


if __name__ == '__main__':
    # print(get_datas('raw_data.csv'))
    # print(get_points())
    write_image('usa.jpg')
