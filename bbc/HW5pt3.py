# Assignment 5
import fileinput

# function that reads population file and builds dictionary
def makeDictionary():
    popDict = {}
    for line in fileinput.input('world_population_2017.tsv'):
        datas = line.split('\t')
        key,population = datas[1],int(''.join(datas[2].split(',')))
        popDict[key] = population
    return popDict

# function that reads drinking water file and prints out
# countries that have changed percentage of people with
# access, if population is big enough.
def readDWdata(popDict):
    print('Country', '1990', '2010', 'Change')
    for index,line in enumerate(fileinput.input('drinkingWater.csv')):
        if index > 2:
            line = line.strip()
            datas = line.split(',')[:-1]
            if '' not in datas:
                zone = datas[0]
                if (zone in popDict) and popDict[zone] > 500000:
                    start = datas[1]
                    end = datas[-1]
                    difference = int(end) - int(start)
                    if difference:
                        print(' '.join((zone,start,end,str(difference))))
    return

def main():
    popDict = makeDictionary()
    readDWdata(popDict)
    return
     
main()