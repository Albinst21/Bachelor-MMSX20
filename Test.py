# A Python program to print all
# permutations using library function
from itertools import permutations
from tabulate import tabulate

# possibilites
nofalse = [True, True, True, True, True]
onefalse = [True, True, True, True, False]
twofalse = [True, True, True, False, False]
threefalse = [True, True, False, False, False]
fourfalse = [True, False, False, False, False]
fivefalse = [False, False, False, False, False]

possibilities = [nofalse, onefalse, twofalse, threefalse, fourfalse, fivefalse]

outcome = []
header = ('S-1,2', 'S-2,1', 'W-1,3', 'W-2,2', 'W-3,1')
for pos in possibilities:
    perm = set(permutations(pos, 5))
    for k in perm:
        outcome.append(k)

dic = dict()
S12 = []
S21 = []
W13 = []
W22 = []
W31 = []
for b in outcome:
    S12.append(b[0])
    S21.append(b[1])
    W13.append(b[2])
    W22.append(b[3])
    W31.append(b[4])

dic['S12'] = S12
dic['S21'] = S21
dic['W13'] = W13
dic['W22'] = W22
dic['W31'] = W31

# Sentences
R1 = 'S21 <-> (W31 or W22)'
R2 = 'S12 <-> (W13 or W22)'

R3 = '(-W13 and -W22) -> W31'

R4 = 'S21'
R5 = '-S12'

TR1 = []
TR2 = []
TR3 = []
TR4 = []
TR5 = []
KB = []

# testing sentences

for k in outcome:
    # Test R1
    if k[1]:
        if k[4] or k[3]:
            TR1.append(True)
        else:
            TR1.append(False)
    if not k[1]:
        if not k[4] and not k[3]:
            TR1.append(True)
        else:
            TR1.append(False)

    # Test R2
    if k[0]:
        if k[2] or k[3]:
            TR2.append(True)
        else:
            TR2.append(False)
    if not k[0]:
        if not k[2] and not k[3]:
            TR2.append(True)
        else:
            TR2.append(False)

    # Test R3
    if k[4] or k[3]:
        if k[3] or k[2]:
            if k[4] or k[2]:
                TR3.append(False)
            else:
                TR3.append(True)
        else:
            TR3.append(True)
    else:
        TR3.append(True)

    # Test R4
    if k[1]:
        TR4.append(True)
    else:
        TR4.append(False)

    # Test R5
    if not k[0]:
        TR5.append(True)
    else:
        TR5.append(False)

for i in range(len(TR1)):
    if TR1[i] and TR2[i] and TR3[i] and TR4[i] and TR5[i]:
        KB.append(True)
    else:
        KB.append(False)

dic['R1: S21 <-> (W31 or W22)'] = TR1
dic['R2: S12 <-> (W13 or W22)'] = TR2
dic['R3: -((W31 or W22) and (W22 or W13) and (W31 or W13))'] = TR3
dic['R4: S21'] = TR4
dic['R5: -S12'] = TR5
dic['KB'] = KB

index = []
for k in range(len(TR1)):
    index.append(k + 1)

table = tabulate(dic, headers='keys', showindex=index)
print(table)
