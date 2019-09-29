# -*- coding:UTF-8


#字体颜色去除
import sys, os
import pytesseract
from PIL import Image, ImageDraw

def test(path):
    img=Image.open(path)
    w,h=img.size
    for x in range(w):
        for y in range(h):
            r,g,b=img.getpixel((x,y))
            # 以下为对指定范围内的颜色的像素全部转为黑色
            if 190<=r<=255 and 170<=g<=255 and 0<=b<=140:
                img.putpixel((x,y),(0,0,0))
            if 0<=r<=90 and 210<=g<=255 and 0<=b<=90:
                img.putpixel((x,y),(0,0,0))
    # 图像转换为灰色图像
    img=img.convert('L').point([0]*150+[1]*(256-150),'1')
    return img

# 循环测试test函数
for i in range(1,13):
    path = str(i) + '.jpg'
    im = test(path)
    path = path.replace('jpg','png')
    im.save(path)

#进行降噪处理

# 二值数组
t2val = {}


def twoValue(image, G):
    for y in range(0, image.size[1]):
        for x in range(0, image.size[0]):
            g = image.getpixel((x, y))
            # 根据像素灰度值与G,分别值将像素坐标及对应的像素，存入t2val字典中
            if g > G:
                t2val[(x, y)] = 1
            else:
                t2val[(x, y)] = 0


# 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
# G: Integer 图像二值化阀值
# N: Integer 降噪率 0 <N <8
# Z: Integer 降噪次数
# 输出
#  0：降噪成功
#  1：降噪失败
def clearNoise(image, N, Z):
    for i in range(0, Z):
        t2val[(0, 0)] = 1
        t2val[(image.size[0] - 1, image.size[1] - 1)] = 1

        for x in range(1, image.size[0] - 1):
            for y in range(1, image.size[1] - 1):
                nearDots = 0
                L = t2val[(x, y)]
                if L == t2val[(x - 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x - 1, y)]:
                    nearDots += 1
                if L == t2val[(x - 1, y + 1)]:
                    nearDots += 1
                if L == t2val[(x, y - 1)]:
                    nearDots += 1
                if L == t2val[(x, y + 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y)]:
                    nearDots += 1
                if L == t2val[(x + 1, y + 1)]:
                    nearDots += 1

                if nearDots < N:
                    t2val[(x, y)] = 1

# 保存文件
def saveImage(filename, size):
    # 创建图像
    image = Image.new("1", size)
    draw = ImageDraw.Draw(image)
    # 循环写入各像素点
    for x in range(0, size[0]):
        for y in range(0, size[1]):
            draw.point((x, y), t2val[(x, y)])
    # 保存图像
    image.save(filename)

for i in range(1,12):
    path =  str(i) + ".png"
    # 转换图像为灰度图
    image = Image.open(path).convert("L")
    twoValue(image, 100)
    # 图像降噪
    clearNoise(image, 3, 2)
    path1 = str(i) + ".jpeg"
    # 保存图像
    saveImage(path1, image.size)


def recognize_captcha(img_path):
    # 打开图片文件
    im = Image.open(img_path)
    # threshold = 140
    # table = []
    # for i in range(256):
    #     if i < threshold:
    #         table.append(0)
    #     else:
    #         table.append(1)
    #
    # out = im.point(table, '1')
    num = pytesseract.image_to_string(im)
    return num


if __name__ == '__main__':
    # 循环识别指定的文件
    for i in range(1, 12):
        img_path = str(i) + ".jpeg"
        res = recognize_captcha(img_path)
        strs = res.split("\n")
        if len(strs) >=1:
            print (strs[0])