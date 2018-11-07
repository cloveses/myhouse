# -*- coding: UTF-8 -*-

import os

def check(data):
    if data.isdigit():
        data = int(data)
        if 0 <= data <= 60:
            return data

def get_data(filename,headlines=5):

    while True:
        k = input("Enter an integer between 0 and 60:")
        k = check(k)
        if k is not None:
            break

    years = []
    temperatures = []
    if not os.path.exists(filename):
        print('File is not exist!')
        return
    datas = None
    with open(filename) as my_file:
        datas = my_file.readlines()[5:]
    if datas:
        datas = [line.strip() for line in datas]
        for data in datas:
            year,temperature = data.split(',')
            years.append(year)
            temperatures.append(float(temperature))
        return k,[years,temperatures]

def save(datas,filename='tempAnomaly.txt'):
    with open(filename,'w') as f:
        for data in datas:
            f.write('\t'.join(data) + '\n')

def main():
    k,datas = get_data('Sacramento-1880-2018.NOAA.csv')
    if datas:
        years,temperatures = datas
        results = [('Year','Value'),]
        for i in range(k,len(years)-k):
            temps = temperatures[i-k:i+k+1]
            results.append((years[i],"{:.4f}".format(sum(temps)/len(temps))))
        save(results)

if __name__ == '__main__':
    main()