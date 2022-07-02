"""
StudentID: 28098552
Name: Ming Shern,Siew
"""
#!/usr/bin/python
import sys
sys.path.append('..')
from Suffix_Tree import SuffixTree

if __name__=="__main__":
    txt = open(sys.argv[1]).read()
    pair = open(sys.argv[2]).read().split()
    newpair = [[0,0] for pairs in range(len(pair)//2)]
    for pairs in range(len(newpair)):
        newpair[pairs][0] = int(pair[pairs * 2])
        newpair[pairs][1] = int(pair[pairs * 2 + 1])
    tree = SuffixTree()
    tree.build(txt+'$')
    for k in range(len(newpair)):
        lcs = tree.longestprefix(newpair[k][0] - 1,newpair[k][1] - 1)
        newpair[k].append(lcs)
    with open('output_lcps.txt', 'w') as outFile:
        for index in range(len(newpair)):
            outFile.write(str(newpair[index][0]) + chr(32) + str(newpair[index][1]) + chr(32) + str(newpair[index][2])  + "\n")
        outFile.close()