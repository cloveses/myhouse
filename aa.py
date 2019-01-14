import os
import datetime
import time
import xlrd
from pony.orm import *

db = Database()

class Taxi(db.Entity):
    textid = Required(str)
    customid = Required(str)
    mtime = Required(int,size=64)
    lat = Required(float)
    lon = Required(float)

class Dataa(db.Entity):
    textid = Required(str)
    customid =Required(str)
    slat = Required(float)
    slon = Required(float)
    elat = Required(float)
    elon = Required(float)

class Datab(db.Entity):
    textid = Required(str)
    mileage = Required(float)
    mtime = Required(int)

db.bind(provider='sqlite', filename='a.db', create_db=True)
db.generate_mapping(create_tables=True)


from math import radians, cos, sin, asin, sqrt
 
def haversine(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
 
    # haversine公式
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # 地球平均半径，单位为公里
    return c * r * 1000


@db_session
def get_datas():
    w = xlrd.open_workbook('taxi.xlsx')
    ws = w.sheets()[0]
    nrows = ws.nrows
    for i in range(nrows):
        data = ws.row_values(i)
        if data[0].strip() and data[1].strip() and isinstance(data[2],float) and \
                isinstance(data[3],float) and isinstance(data[4],float):

            Taxi(textid=data[0].strip(), customid=data[1].strip(), 
                mtime=int(data[2]), lat=data[3], lon=data[4])

@db_session
def deal():
    taxiids = select(t.textid for t in Taxi)
    for taxiid in taxiids:
        ataxi_datas = select(t for t in Taxi if t.textid == taxiid).order_by(Taxi.mtime)[:]
        start = 0
        cur_custom = ataxi_datas[start].customid
        for i in range(1,len(ataxi_datas)):
            if ataxi_datas[i].customid != cur_custom:
                Dataa(textid=taxiid, customid=cur_custom, 
                    slat=ataxi_datas[start].lat, slon=ataxi_datas[start].lon, 
                    elat=ataxi_datas[i-1].lat, elon=ataxi_datas[i-1].lon)
                start = i
                cur_custom = ataxi_datas[i].customid
                Datab(textid=taxiid, mileage=haversine(ataxi_datas[i-1].lat, ataxi_datas[i-1].lon,
                    ataxi_datas[i].lat, ataxi_datas[i].lon), mtime=ataxi_datas[i].mtime-ataxi_datas[i-1].mtime)
        else:
            Dataa(textid=taxiid, customid=cur_custom, 
                slat=ataxi_datas[start].lat, slon=ataxi_datas[start].lon, 
                elat=ataxi_datas[i].lat, elon=ataxi_datas[i].lon)

@db_session
def get_res():
    with open('da.txt','w') as f:
        for d in select(da for da in Dataa):
            f.write(d.textid)
            f.write(',')
            f.write(d.customid)
            f.write(',')
            f.write(str(d.slat))
            f.write(',')
            f.write(str(d.slon))
            f.write(',')
            f.write(str(d.elat))
            f.write(',')
            f.write(str(d.elon))
            f.write('\n')

    with open('db.txt','w') as f:
        for d in select(dbb for dbb in Datab):
            f.write(d.textid)
            f.write(',')
            f.write(str(d.mileage))
            f.write(',')
            f.write(str(d.mtime))
            f.write('\n')

if __name__ == '__main__':
    # get_datas()
    # deal()
    # get_res()
    # print(haversine(113.973129, 22.599578, 114.3311032, 22.6986848))