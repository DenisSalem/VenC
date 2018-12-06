#! /usr/bin/python
import time

iteration = 10000

string = ".:foo::bar:. .:IfInThread:: .:boo:: .:foo::bar:. :. :: lolilol :. .:END:. .:TEST AGAIN:: .:WITHIN:. :."
string = ".:IfInThread::<link rel=\"stylesheet\" href=\".:GetRelativeOrigin:.styleThread.css\" type=\"text/css\" />::<link rel=\"stylesheet\" href=\".:GetRelativeOrigin:.styleEntry.css\" type=\"text/css\" />:."
def algo1():
    op = []
    cp = []
    i = 0
    l = len(string)
    output = string
    offset=0
    while i < l:
        i = output.find(".:", i)
        if i == -1:
            i=0
            break
        op.append(i)
        i+=2
    
    while i < l:
        i = output.find(":.", i)
        if i == -1:
            i=0
            break
        cp.append(i)
        i+=2

    lo = len(op)
    lc = len(cp)
    if lo != lc:
        raise Exception
    while lo:
        diff = 18446744073709551616
        i = 0
        j = 0
        for io in range(0, lo):
            for ic in range(0, lc):
                d = cp[ic] - op[io]
                if d > 0 and d < diff:
                    diff = d
                    i = io
                    j = ic

        vop, vcp = op[i], cp[j]
        fields = [field.strip() for field in output[vop+2:vcp].split("::") if field != '']
        new_string = "["+'---'.join(fields)+"]"
        # d0 shit there

        output = output[0:vop] + new_string + output[vcp+2:]
        offset = len(new_string) - (vcp + 2 - vop)
        for k in range(1,lo):
            if k >= i+1:
                op[k]+=offset

            cp[k]+=offset

        op.pop(i)
        cp.pop(j)
        lo -= 1
        lc -= 1
                
    return output

def algo2(string):
    op = []
    cp = []
    l = len(string)
    fields=[]
    for i in range(0, l):
        if string[i:i+2] == ".:":
            op.append(i)    
        
        elif string[i:i+2] == ":.":
            cp.append(i)
            
        if len(cp) <= len(op) and len(cp) != 0 and len(op) != 0:
            if op[-1] < cp[-1]:
                fields = [field.strip() for field in string[op[-1]+2:cp[-1]].split("::") if field != '']
                
                return algo2(string[:op[-1]]+"["+'---'.join(fields)+"]"+string[cp[-1]+2:])

    return string

t = time.time()
for i in range(0,iteration):
    c = algo1()

print(c)

print("ALGO1", time.time()-t)
t = time.time()
for j in range(0,iteration):
    s = algo2(string)
print(s)
print("ALGO2", time.time()-t)
