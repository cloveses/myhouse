import re

class program:
    def __init__(self, s):
        self.progs = s
        self.vars = {}
        self.blocks = {}
        self.graphs = {}

    def get_var(self, vars):
        i = 0
        while True:
            s = vars[i]
            if s.startswith('bool'):
                position = s.index('=')
                self.vars[s[:position].replace('bool','').strip()] = eval(s[position+1:].strip().strip(';'))
                i += 1
            else:
                break
        return i

    # def get_index(self, progs, keys=('if','fi','while','done'), indent=0):
    #     positions  = []
    #     for index,prog in enumerate(progs):
    #         if prog in keys:
    #             positions.append(index)
    #     if positions:
    #         positions = [(p[i],p[i+1]) for p in range(0,len(positions),2)]
    #     return positions

    def parse(self, progs):
        pre_link = -1
        block = []
        for prog in progs:
            if ':' in prog:
                label,stmt = prog[:prog.index(':')],prog[prog.index(':')+1:]
                if 'if' in prog:
                    block.append((label,stmt.strip(';')))
                    self.blocks[block[0][0]] = block[:]
                    pre_link = block[0][0]
                    self.graphs[block[0][0]] = label
                    block = []

                elif 'while' in prog:
                    if block:
                        self.blocks[block[0][0]] = block[:]
                        self.graphs[block[0][0]] = label
                    self.blocks[label] = [(label,stmt),]
                    pre_link = label
                    block = []

                else:
                    block.append((label,stmt.strip(';')))

            else:
                if block:
                    self.blocks[block[0][0]] = block[:]
                    self.graphs[pre_link] = block[0][0]
                    if prog.strip() == 'done':
                        self.graphs[block[0][0]] = pre_link

                    block = []
        if block:
            self.graphs[block[0][0]] = label
            self.blocks[pre_link] = block[:]
        print(self.blocks)
        print(self.graphs)



    def getCFG(self):
        progs = self.progs.split('\n')
        progs = [prog.strip() for prog in progs if prog.strip()]
        
        fun_start = self.get_var(progs)
        progs = progs[fun_start+1:]
        progs = [prog for prog in progs if prog not in  ['main()','{','}'] ]
        self.parse(progs)

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
4:     y= !y;
5:     pass;
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
p.getCFG()