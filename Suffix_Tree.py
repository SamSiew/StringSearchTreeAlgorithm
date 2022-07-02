"""
StudentID: 28098552
Name: Ming Shern,Siew
"""
class SuffixNode:
    def __init__(self, start=-1, end=None, suffixID=-1):
        self.children = [None] * 128
        self.suffix_link = None
        self.start = start
        self.end = end
        self.stop_index = -1
        self.suffixID = suffixID

    def __getitem__(self, item):
        return self.children[ord(item)]

    def __setitem__(self, key, value):
        self.children[ord(key)] = value

    def get_edge_length(self):
        return self.get_end_index() - self.start + 1

    def get_end_index(self):
        if self.stop_index < 0:
            return self.end.index
        else:
            return self.stop_index

class End:
    def __init__(self, index=None):
        self.index = index

class Active:
    def __init__(self, node):
        self.node = node
        self.edge = -1
        self.edge_2 = -1
        self.child = -1
        self.length = 0

class SuffixTree:
    def __init__(self):
        self.root = SuffixNode(-1, End(-1))
        self.active = Active(self.root)
        self.end = End(-1)
        self.string = ""
        self.length = 0
        self.remainder = 0

    def __len__(self):
        return self.length

    def get_all_edge(self):
        """
        Debugging code used to test longest prefix

        :return: memo of all edges
        """
        memo = []
        self.tranverse_edge(self.root, memo)
        return memo

    def tranverse_edge(self, node, memo):
        """
        Tranverse all edges

        :param node: starting node
        :param memo: memo of all edges
        :return: memo of all edges
        """
        for i in range(len(node.children)):
            if node.children[i] != None:
                memo.append([node.children[i].start, node.children[i].get_end_index()])
                self.tranverse_edge(node.children[i], memo)

    def wild_card(self, pat):
        """
        first, search all occurances with suffix tree
        then, mark the occurance on memo to indicate presence.

        Note: memorization for '?' could be good device but it is trade off from time,
        unless it affect the time complexity and do not affect string of million character ->
        would be a elegant way, but it is too expensive for space complexity.
        The worst case is when all wild card and if each edge only consist of one character, then memorization
        would not do anything at this point.
        Thus, memorization which will helps to reduce time complexity by large margin will be worth implement but
        if it not does anything, then, it redundant and very expensive.

        :param pat: pattern
        :return: retmemo, array of binary indicating start position till occurance
        """
        memo = []
        self.wild_card_search(pat, self.root, 0, 0, 0, memo)
        retmemo = [0 for i in range(len(self.string) - 1)]
        for i in range(len(memo)):
            retmemo[memo[i]] = 1
        return retmemo

    def wild_card_search(self, pat, node, pat_index, edge_index, sublength, memo):
        """
        if node is root or current position of edge labels goes passed end of node:
            if current pattern is wild card:
                Tranverse all children
            else:
                if next node has edge which correspond to character:
                    tranverse down the path to look for more character
                else
                    backtrack by return
        else
            if current pattern is wild card or text[k] == pat[j]:
                if edge label go passed edge:
                    add to sublength to add up number of character matches
                if current pat reach end of pat:
                    if it is leaf: add to array if sublength is not equal to len(pat)-> to ensure $ not included
                    else: go through all suffixes and gather its suffix id
                    backtrack by return
                tranverse down the path to look for more character
            else
                backtrack by return

        :param pat: pattern
        :param node: starting node to tranverse
        :param pat_index: position of pat
        :param edge_index: position at edge
        :param sublength: length of substrings -> used to exclude $
        :param memo: array to collect result
        :return: nothing
        """
        """
        if node is root or current position of edge labels goes passed end of node:
            if current pattern is wild card:
                Tranverse all children
            else:
                if next node has edge which correspond to character:
                    tranverse down the path to look for more character
                else
                    backtrack by return
        """
        if node.start == -1 or (edge_index > node.get_edge_length() - 1):
            if pat[pat_index] == '?':
                for i in range(len(node.children)):
                    if node.children[i] != None:
                        self.wild_card_search(pat, node.children[i], pat_index, 0, sublength, memo)
            else:
                if node[pat[pat_index]] != None:
                    self.wild_card_search(pat, node[pat[pat_index]], pat_index, 0, sublength, memo)
                else:
                    return
        else:
            """
            if current pattern is wild card or text[k] == pat[j]:
                if edge label go passed edge:
                    add to sublength to add up number of character matches
                if current pat reach end of pat:
                    if it is leaf: add to array if sublength is not equal to len(pat)-> to ensure $ not included
                    else: go through all suffixes and gather its suffix id
                    backtrack by return
                tranverse down the path to look for more character
            else
                backtrack by return
            """
            if pat[pat_index] == '?' or self.string[node.start + edge_index] == pat[pat_index]:
                if edge_index + 1 > node.get_edge_length() - 1:
                    sublength += edge_index + 1
                if pat_index + 1 == len(pat):
                    if node.stop_index < 0:
                        if sublength != len(pat):
                            memo.append(node.suffixID)
                    else:
                        # find all leaf
                        self.get_all_suffix(node, memo)
                    return
                self.wild_card_search(pat, node, pat_index + 1, edge_index + 1, sublength, memo)
            else:
                return

    def build_suffix_array(self):
        """
        This will return suffix array with help of in-order tranversal of tree to get suffix id

        :return: suffix array, array of suffix ID
        """
        suffixArray = []
        self.get_all_suffix(self.root, suffixArray)
        return suffixArray

    def get_all_suffix(self, node, array):
        """
        This will use in-order tranversal of tree to get suffix id

        :param node: starting node to tranverse
        :param array: array to collect suffix id
        :return: nothing
        """
        #look for all children
        for i in range(len(node.children)):
            child = node.children[i]
            #as long as they not null, we know there's a node we can tranverse to the leaf
            if child != None:
                if child.stop_index < 0:
                    array.append(child.suffixID)
                self.get_all_suffix(node.children[i], array)

    def longestprefix(self, i, j):
        """
        The approach exploit the fact that given substring, longest prefix of substring[i...j]
        is also longest suffix of substring[i...j] which matches prefix.

        :param i: position of suffix i
        :param j: position of suffix j
        :return: common prefix suffix i to j
        """
        currentNode = self.root[self.string[j]]
        #offset indicete longest length which we need to go down the string
        offset = 0
        """
        while sum(j,length of longest prefix in previous iteration) < length of string and if next i, j suffixes maches do
            add offset with length of edges
            tranverse down the node
        """
        while j + offset < len(self.string) and self.string[i + offset] == self.string[j + offset]:
            offset += currentNode.get_edge_length()
            currentNode = currentNode[self.string[j + offset]]
        return offset

    def skip_count(self, node, remainder, j):
        """
        As long as there are suffixes left, tranverse down deepest path.

        :param node: current to tranverse
        :param remainder: number of time to tranverse
        :param j: original location to tranverse
        :return: [node, remainder] where, n is deepest node it can tranverse from remainder and
                 remainder is edges that are needed to tranverse
        """
        if remainder > node.get_edge_length():
            self.active = Active(node)
            self.active.child = j + node.get_edge_length()
            return self.skip_count(node[self.string[j + node.get_edge_length()]], remainder - (node.get_edge_length()), j + node.get_edge_length())
        else:
            self.active.length += remainder
            return [node, remainder]

    def build(self, string):
        """
        Construct Implicit Tree
        For i from 1 to m — 1 do
            begin [phase i + 1}
            For j from 1 to i + 1 do
                begin {extension j}
                Find the end of the path from the root labeled S[j..i] in the
                current tree.
                Extend that path by adding character S[i + 1) using rule 1|2|3
                end {extension j}
            end;
        end;

        :param string: string for tree to build
        :return: nothing
        """
        self.string = string
        self.active = Active(self.root)
        j = 0
        for i in range(len(self.string)):
            """
            rule 1: extend the edges.
            """
            self.end.index += 1
            lastNewNode = None
            while j < i + 1:
                """
                if length of active node = 0
                    start from root
                    look for string[j] in active node children
                    if exist: 
                        continue to tranverse down 
                    else:
                        create new internal node(rule 2, no split)
                """
                if self.active.length == 0:
                    self.active = Active(self.root)
                    if self.active.node[self.string[j]] != None:
                        self.active.child = j
                        current = self.active.node[self.string[j]]
                        k = j
                    else:
                        self.active.node[self.string[j]] = SuffixNode(i, self.end, j)
                        self.active.edge = j
                        j += 1
                        continue
                else:
                    current = self.active.node[self.string[self.active.child]]
                    k = self.active.edge

                retval = [current, 0]
                """
                perform skip count if and only if remaining > 0
                """
                if i - k > 0: retval = self.skip_count(current, (i - k), k)
                current = retval[0]
                """
                continue from last edge label from j-1 iteration or previous phase.
                """
                if self.active.edge_2 > -1:
                    pointer = self.active.edge_2
                else:
                    pointer = current.start + retval[1]
                k = i
                """
                if edges label goes beyond edges:
                    if current node has no edges for children which correspond to edge label:
                        create new internal node(rule 2, no split)
                    else
                        move active node and current node by one step
                """
                if pointer > current.get_end_index():
                    if current[self.string[k]] == None:
                        current[self.string[k]] = SuffixNode(k, self.end, j)
                        self.active = Active(self.root)
                        j += 1
                        continue
                    else:
                        self.active = Active(current)
                        self.active.child = k
                        current = current[self.string[k]]
                        pointer = current.start
                """
                if string[k] == string[pointer]:
                    split the edges(rule 2)
                else:
                    go to next phase with j remains(rule 3)
                    exploit active node activity by not moving to root
                """
                if self.string[k] != self.string[pointer]:
                    parentnode = self.active.node
                    newnode = SuffixNode(current.start, self.end, j - 1)
                    newnode.stop_index = pointer - 1
                    newnode.suffix_link = self.root
                    childpos = current.start
                    current.start = pointer
                    newnode[self.string[pointer]] = current
                    newnode[self.string[k]] = SuffixNode(k, self.end, j)
                    parentnode[self.string[childpos]] = newnode
                    if lastNewNode != None:
                        lastNewNode.suffix_link = newnode
                    lastNewNode = newnode
                    """
                    Tried to start from suffix link, but has bugs which can discrupt whole assignment:
                    
                    if active node has no suffix link:
                      go to root and start to extend on next phase
                    else
                      go to suffix link of active node 
                    
                    After moving to new nodes, the alpha of old node and alpha of new node are the same
                    meaning they both share same prefix. Then, it should start comparing a point where let say beta,b 
                    or better suffixes which start after alpha of both node will need to be used with 
                    skip_count function, remainder and active node till position i and extends str[i+1] if str[i+1] is 
                    nowhere be found.  
                    
                    If the path str[j..i] in implicitSuffixTree does NOT end at a leaf, 
                    and the next character in the existing path is some k != str[i + 1], 
                    and str[i] and k are to be separated by new internal node u.
                    
                    Previous newly created internal node is to be linked from node u.   
                    
                    The suffix link implementation is last piece of this program and would have taken it to O(n).
                    """
                    # if parentnode.suffix_link == None:
                    #     self.active = Active(self.root)
                    #     self.active.edge = j + 1
                    # else:
                    #     self.active = Active(parentnode.suffix_link)
                    #     self.active.edge = i - j
                else:
                    """
                    rule 3 and show stopper.
                    """
                    self.active.edge = k
                    self.active.length = pointer - current.start
                    self.active.edge_2 = pointer + 1
                    break
                self.active = Active(self.root)
                j += 1