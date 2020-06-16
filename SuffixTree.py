numbers = {str(i) for i in range(0, 10, 1)}

class Data:
    def __init__(self, s, belong2Index = None):
        super().__init__()
        self.s = s
        self.belong2Index = belong2Index
    
    def belongs(self):
        return len(self.belong2Index) if self.belong2Index else 0

    def addBelong(self, belong, index=None):
        self.belong2Index[belong] = index

class Node:
    def __init__(self, data, parent, childs = None):
        super().__init__()
        self.data = data
        self.parent = parent
        if childs is None:
            childs = {}
        self.childs = childs
    
    def addChild(self, key, child):
        self.childs[key] = child
    
    def removeChild(self, key):
        del self.childs[key]

    def replaceChild(self, key, newChild):
        self.childs[key] = newChild

    def isLeaf(self):
        return self.parent and len(self.childs) == 0

    def isRoot(self):
        return not self.parent

    def __eq__(self, value):
        if isinstance(value, Node):
            return self.data.s == value.data.s
        return False

    def __str__(self, prefix=''):
        s = prefix + self.data.s + ':' + str(self.data.belongs()) + ':' + str(self.data.belong2Index)
        for child in self.childs.values():
            s += '\n'
            s += child.__str__(prefix + '    ')
        return s

class Suffix:
    def __init__(self, string, index, belong):
        super().__init__()
        self.index = index
        self.belong = belong
        self.string = string


class SuffixTree:
    def __init__(self, stringList):
        super().__init__()
        self.stringList = stringList
        self.root = Node(Data('root'), None)

    def findPattern(self, pattern):
        root = self.root
        start = 0
        while True:
            if start >= len(pattern) :
                return 'Pattern Found'
            if pattern[start] not in root.childs:
                return 'Pattern Not Found'
            child = root.childs[pattern[start]]
            minLen = min(len(child.data.s), len(pattern) - start)
            if pattern[start:start + minLen] != child.data.s[0:minLen]:
                return 'Pattern Not Found'
            start += len(child.data.s)
            root = child

    def findLongestPalindromicSubString(self):
        return self.longestSubString(self.root, len(self.stringList))

    def isPalindromicSubString(self, node, length):
        if not node.data.belong2Index or not node.data.belong2Index[0] or not node.data.belong2Index[1]:
            return True
        reversedEndIndexInOriginal = len(self.stringList[1]) - 1 - node.data.belong2Index[1]
        reversedStartIndexInOriginal = reversedEndIndexInOriginal - length + 1
        return node.data.belong2Index[0] == reversedStartIndexInOriginal and node.data.belong2Index[0] + length - 1 == reversedEndIndexInOriginal

    def longestSubString(self, node, belongs):
        if not node.isRoot() and node.data.belongs() != belongs:
            return ''

        if len(node.childs) == 0:
            return ''
            
        subString = ''
        for child in node.childs.values():
            s = node.data.s + self.longestSubString(child, belongs)
            if s and len(s) > len(subString) and self.isPalindromicSubString(node, len(s)):
                subString = s
        return subString if not node.isRoot() else subString[4:]
            

    def build(self):
        suffixes = self.generateSuffixes()
        for suffix  in suffixes:
            self.buildSingleString(self.root, suffix)
        self.compress(self.root)
        print(self.root)

    def compress(self, root):
        if root.isLeaf():
            return
        if not root.isRoot() and len(root.childs) == 1:
            child = list(root.childs.values())[0]
            tempNode = Node(Data(root.data.s + child.data.s, root.data.belong2Index), root.parent, child.childs)
            root.parent.replaceChild(root.data.s[0], tempNode)
            self.compress(tempNode)
        else:
            for child in root.childs.values():
                self.compress(child)

    def buildSingleString(self, root, suffix, start=0):
        if start >= len(suffix.string):
            return
        string = suffix.string[start:]
        index = suffix.index + start
        # base case : tail 
        if self.isTail(string):
            root.addChild(suffix, Node(Data(string, {suffix.belong : index}), root))
            return
        thisChar = string[0]
        next = self.findPath(root, thisChar)
        # no path starts with s[start]
        if not next:
            startRoot = Node(Data(thisChar, {suffix.belong : index}), root)
            root.addChild(thisChar, startRoot)
            self.buildSingleString(startRoot, suffix, start + 1)
            return
        # exist path starts wirht s[start]
        next.data.addBelong(suffix.belong, index)
        self.buildSingleString(next, suffix, start + 1)
     
    def findPath(self, root, c):
        return root.childs[c] if c in root.childs else None

    def isTail(self, s):
        if len(s) <= 1 or s[0] != '$':
            return False
        for i in range(1, len(s), 1):
            if s[i] not in numbers:
                return False
        return True

    def getTailNumber(self, s):
        for i in range(len(s) - 1, -1, -1):
            if s[i] == '$':
                return s[i+1:]
        raise Exception('No Valid Tail Found')

    def generateSuffixes(self):
        suffixes = []
        for i in range(len(self.stringList)):
            suffixes += self.generateSuffixesOfSingleString(i, self.stringList[i], '${}'.format(i))
        return suffixes
        
    def generateSuffixesOfSingleString(self, belong, s, tail):
        return [Suffix(s[i:] + tail, i, belong) for i in range(len(s))]

    def __str__(self):
        if not self.root or len(self.root.childs) == 0:
            return 'Empty Suffix Tree'
        
#tree = SuffixTree(['bear', 'bell', 'bid', 'bull', 'buy', 'sell', 'stock', 'stop'])
tree =SuffixTree(['abacdfgdcaba', 'abacdgfdcaba'])
tree.build()
print(tree.findLongestPalindromicSubString())


