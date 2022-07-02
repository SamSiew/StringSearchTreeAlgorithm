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
    pattern = open(sys.argv[2]).read()
    tree = SuffixTree()
    tree.build(txt+'$')
    output = tree.wild_card(pattern)
    with open('output_wildcard_matching.txt', 'w') as outFile:
        for index in range(len(output)):
            if output[index] == 1:
                outFile.write(str(index + 1) + "\n")
        outFile.close()