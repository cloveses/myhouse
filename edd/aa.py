class program:
    def __init__(self,s):
        self.progs = s
        self.labels = []
        self.parse_stutas = 0

    def getCFG(self):
        pass
        progs = self.progs.split('\n')
        for line in progs:
            if line:
                if 


    def evaluate(self):
        pass


s="""
bool x = True;
bool y = False;
bool z = True;
bool a = True;
main()
{
1: x= !y;
2: z= !x;
3: if ( (x & y) | (! z) )
4: y= !y;
5: pass;
fi
6: x=!y;
7: z=!z;
8: while ( ( x | y) & (a | z) )
9: a=!y;
10: y=!z;
done
11: return x;
}
"""
p = program(s)