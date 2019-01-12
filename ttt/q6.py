def tokens(string,seps):
    while string.find(seps) != -1:
        yield string[:string.index(seps)]
        string = string[string.index(seps)+1:]
    yield string

def test():
    for s in tokens('aaa,bbb,ccc,dddd,eeee,kkkk',','):
        print(s)

test()