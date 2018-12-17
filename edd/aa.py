class program:
    def __init__(self,s):
        self.progs = s
        self.blocks = {}
        self.parse_stutas = 0
        self.variables = dict()
        self.graph = dict()

    def parse(self, stmts):
        stmts = [s for s in stmts if s]
        block = []
        for stmt in stmts:
            words = stmt.split(' ')
            block.append(stmt.split(':'))
            if 'if' in words or 'while' in words:
                self.blocks[block[0][0]] = block[:]
                block = []
                



    def getCFG(self):
        progs = self.progs.split('\n')
        for line in progs:
            if line:
                if self.parse_stutas == 0:
                    if line == '{' or line.startswith('main()'):
                        self.parse_stutas = 1
                        continue
                    elif line == '}':
                        break
                    else:
                        if line.startswith('bool'):
                            segments = line.strip().split(' ')
                            segments = [s for s in segments if s]
                            self.variables[segments[1]] = eval(segments[-1].strip(';'))
                if self.parse_stutas == 1:
                    self.graph

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