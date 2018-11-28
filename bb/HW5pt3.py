# Assignment 5
import fileinput

# function that reads population file and builds dictionary
def makeDictionary():
    res = {}
    for line in fileinput.input('world_population_2017.tsv'):
        datas = line.split('\t')
        key,value = datas[1],datas[2]
        res[key] = int(''.join(value.split(',')))
    # print(res)
    return res

# function that reads drinking water file and prints out
# countries that have changed percentage of people with
# access, if population is big enough.
def readDWdata(popDict):
    print('Country','\t','1990','\t','2010','\t','Change')
    for index,line in enumerate(fileinput.input('drinkingWater.csv')):
        if index > 2:
            datas = line.split(',')[:-1]
            country = datas[0]
            data = [d.strip() for d in datas[1:]]
            if not ('' in data):
                data = [int(d) for d in data if d]
                cflag = country in popDict and popDict[country] > 500000 and data[0] != data[-1]
                if cflag:
                    print(datas[0], '\t', data[0], '\t', data[-1], '\t', data[-1]-data[0])
    return

def main():
    popDict = makeDictionary()
    readDWdata(popDict)
    return
     
main()
