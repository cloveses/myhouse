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
    return

def main():
    popDict = makeDictionary()
    print(popDict)
    return
     
main()
