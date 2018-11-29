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
    return

def main():
    return
     
main()
