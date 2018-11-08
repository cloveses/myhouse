# -*- coding: UTF-8 -*-

import os

def check(data):
    if data.isdigit():
        data = int(data)
        if 0 <= data <= 60:
            return data

def get_data(filename,headlines=5):

    years = []
    temperatures = []

    datas = None
    try:
        with open(filename) as my_file:
            datas = my_file.readlines()[5:]
    except:
        print('The file %s could not be opened.' % filename)
        return

    while True:
        k = input("Enter an integer between 0 and 60:")
        k = check(k)
        if k is not None:
            break

    if datas:
        datas = [line.strip() for line in datas]
        for data in datas:
            year,temperature = data.split(',')
            years.append(year)
            temperatures.append(float(temperature))
        return k,years,temperatures

def save(datas,filename='tempAnomaly.txt'):
    with open(filename,'w') as f:
        for data in datas:
            f.write('\t'.join(data) + '\n')

def main():
    filename = None
    while True:
        filename = input('Temperature anomaly filename:')
        if filename:
            break
    res = get_data(filename)
    if res:
        k,years,temperatures = res
        results = [('Year','Value'),]
        for i in range(k,len(years)-k):
            temps = temperatures[i-k:i+k+1]
            results.append((years[i],"{:.4f}".format(sum(temps)/len(temps))))
        save(results)

if __name__ == '__main__':
    main()