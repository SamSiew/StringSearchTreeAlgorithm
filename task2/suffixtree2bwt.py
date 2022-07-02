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
    tree = SuffixTree()
    tree.build(txt+'$')
    output = tree.build_suffix_array()
    with open('output_bwt.txt', 'w') as outFile:
        for index in range(len(output)):
            if output[index] != 0:
                outFile.write(txt[output[index] - 1])
            else:
                outFile.write('$')
        outFile.close()