def naive_suffix(s):
    return [t[1] for t in sorted((s[i:],i) for i in range(len(s)))]
class SuffixNode:
    def __init__(self,start=-1,end=-1,suffixID=-1):
        self.parent = None
        self.children = [None] * 128
        self.start = start
        self.end = end
        self.suffixID = suffixID

    def __getitem__(self, item):
        return self.children[ord(item)]

    def __setitem__(self, key, value):
        self.children[ord(key)] = value
        value.parent = self

    def get_edge_length(self):
        return self.end - self.start

    def copy(self):
        item = SuffixNode(self.start, self.end)
        item.parent = self.parent
        item.children = self.children
        item.suffixID = self.suffixID
        return item

class SuffixTree:
    # Trie data structure class
    def __init__(self):
        self.root = SuffixNode()
        self.string = ""

    def get_all_edge(self):
        memo = []
        self.tranverse_edge(self.root, memo)
        return memo

    def tranverse_edge(self, node, memo):
        for i in range(len(node.children)):
            if node.children[i] != None:
                memo.append([node.children[i].start, node.children[i].end])
                self.tranverse_edge(node.children[i], memo)

    def wild_card(self,pat):
        memo = []
        wildCardMemo = [0 for i in range(len(pat))]
        for i in range(len(pat)-1,-1,-1):
            if pat[i] == '?':
                wildCardMemo[i] = 1
                if i < len(pat)-1:
                    wildCardMemo[i] += wildCardMemo[i + 1]

        self.wild_card_search(pat,self.root,0,0,0,memo)
        retmemo = [0 for i in range(len(self.string)-1)]
        for i in range(len(memo)):
            retmemo[memo[i]] = 1
        return retmemo

    def wild_card_search(self,pat,node,pat_index,edge_index,sublength,memo):
        if node.start == -1 or (edge_index > node.get_edge_length()):
            if pat[pat_index] == '?':
                for i in range(len(node.children)):
                    if node.children[i] != None:
                        self.wild_card_search(pat, node.children[i], pat_index, 0,sublength,memo)
            else:
                if node[pat[pat_index]] != None:
                    self.wild_card_search(pat,node[pat[pat_index]],pat_index, 0,sublength, memo)
                else:
                    return
        else:
            if pat[pat_index] == '?' or self.string[node.start + edge_index] == pat[pat_index]:
                if edge_index + 1 > node.get_edge_length():
                    sublength += edge_index + 1
                if pat_index + 1 == len(pat):
                    if node.suffixID >= 0:
                        if sublength != len(pat):
                            memo.append(node.suffixID)
                    else:
                        #find all leaf
                        self.get_all_suffix(node, memo)
                    return
                self.wild_card_search(pat, node, pat_index + 1, edge_index + 1, sublength, memo)
            else:
                return

    def build_suffix_array(self):
        suffixArray = []
        self.get_all_suffix(self.root,suffixArray)
        return suffixArray

    def get_all_suffix(self,node,array):
        for i in range(len(node.children)):
            child = node.children[i]
            if child != None:
                if child.suffixID >= 0:
                    array.append(child.suffixID)
                self.get_all_suffix(node.children[i], array)

    def longestprefix(self,i,j):
        currentNode = self.root[self.string[j]]
        offset = 0
        while j + offset < len(self.string) and self.string[i+offset] == self.string[j+offset]:
            offset += currentNode.get_edge_length() + 1
            currentNode = currentNode[self.string[j+offset]]
        return offset

    def build(self,string):
        self.string += string
        n = len(string)
        for i in range(n):
            currentNode = self.root
            if currentNode[self.string[i]] == None:
                currentNode[self.string[i]] = SuffixNode(i,n-1,i)
            else:
                currentNode = currentNode[self.string[i]]
                j = currentNode.start
                k = i
                while k < n :
                    if j <= currentNode.end:
                        if self.string[k] != self.string[j]:
                            if j == currentNode.start:
                                currentNode[self.string[k]] = SuffixNode(k, n - 1, i)
                            else:
                                parentnode = currentNode.parent
                                newnode = SuffixNode(currentNode.start, j - 1)
                                tempnode = currentNode.copy()
                                tempnode.start = j
                                newnode[self.string[j]] = tempnode
                                newnode[self.string[k]] = SuffixNode(k, n - 1, i)
                                parentnode[self.string[currentNode.start]] = newnode
                            k = n
                    else:
                        if currentNode[self.string[k]] == None:
                            currentNode[self.string[k]] = SuffixNode(k, n - 1, i)
                            k = n
                        else:
                            currentNode = currentNode[self.string[k]]
                            j = currentNode.start
                    j += 1
                    k += 1

if __name__== '__main__':
    new = SuffixTree()
    new.build('AAABAAAABAAACAAABAAAA$')
    #new.build('srdvsmaphgifibnneitxjqyqvfpchpczffvlwhhhh$')
    print(new.build_suffix_array())
    print(naive_suffix(new.string))