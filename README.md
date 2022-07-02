# StringSearchTreeAlgorithm

**SuffixTree**: Compressed trie containing all the suffixes of the given text and is build efficiently with Ukkonen's algorithm.
</br>**Ukkonen's algorithm**: Linear-time, online algorithm for constructing suffix trees, proposed by Esko Ukkonen. The algorithm begins with an implicit suffix tree containing the first character of the string. Then it steps through the string, adding successive characters until the tree is complete. This order addition of characters gives Ukkonen's algorithm its "on-line" property.
</br>**Burrows–Wheeler transform**: Algorithm which rearranges a character string into runs of similar characters. This is useful for compression, since it tends to be easy to compress a string that has runs of repeated characters.
</br>**LCP array**: Longest common prefix array (LCP array) is an auxiliary data structure to the suffix array. It stores the lengths of the longest common prefixes (LCPs) between all pairs of consecutive suffixes in a sorted suffix array.
