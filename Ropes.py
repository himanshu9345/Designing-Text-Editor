# node to store information in Ropes
class Node():
    weight = 0
    text = ""
    left = None
    right = None
    parent = None
    
    def __init__(self, str1, size, par = None):
        self.weight = size
        self.text = str1
        self.parent = par
    
    def __str__(self):
        str1 = "Node Info { " + "text : "+ self.text + " weight: "+ str(self.weight)+" }"
        return str1



# main class to handle string manipulation
class Rope(object):
    LEAF_SIZE = 3
    root = None
    
    def __init__(self, document):
        self.root, sum1 = self.createRopes(document, 0, len(document) - 1, None)
        self.root1, sum1 = self.createRopes("document", 0, len("document") - 1, None)

        # print("ggg")
        # self.printTree(self.root)
        # print(self.searchIndex(self.root, 10))
        # self.printTree(self.concatenationOperation(self.root, self.root1))
        self.split(self.root,7)
    
    def createRopes(self, str1, start, end, parent):
        node = Node("", -1)
        node.parent = parent
        if end - start > self.LEAF_SIZE:
            mid = start + (end - start)//2
            # node.weight = 
            node.left, sum1 = self.createRopes(str1, start, mid, node)
            node.right, sum2 = self.createRopes(str1, mid + 1, end, node)
            node.weight = sum1
            return node, sum1 + sum2
        else:
            node.weight = end - start + 1
            node.text = str1[start:end+1]
            return node, node.weight

    def searchIndex(self, node, index):
        # print(index, node.text)
        
        if node.weight < index:
            return self.searchIndex(node.right, index - node.weight)
        if not node.right and not node.left:
            return node.text[index-1]
        
        return self.searchIndex(node.left,  index)
    
    def searchIndexReturnNode(self, node, index):
        # print(index, node.text)

        if node.weight < index:
            return self.searchIndexReturnNode(node.right, index - node.weight)
        if not node.right and not node.left:
            return node, index-1
        
        return self.searchIndexReturnNode(node.left,  index)
    
    # could be optimize if we used balanced tree
    def concatenationOperation(self, left_node, right_node):
        new_node = Node("", -1)
        new_node.left = left_node
        new_node.right = right_node
        left_node.parent = new_node
        right_node.parent = new_node
        new_node.weight = self.getWeight(left_node)
        return new_node
    
    # still doublt if i needed this, since i have perent nodes
    def getWeight(self, node):
        if not node.left and not node.right:
            return node.weight
        return self.getWeight(node.left) + self.getWeight(node.right)  

    def split(self, node, index):
        node_to_split, split_position = self.searchIndexReturnNode(node, index)
        '''
        if char from which split has to happen, 
        - if its in the middle divide current node string to two parts and then create
            a new node which will be parent of tow component nodes
        
        if splitting char is at 0 index the dont do any thing

        Main Logic
        - the current node(from where split has to happen) go to it parent's parent and substract 
        the weight of current node then remove any right link of the subtree covering charcter past index


        
        '''
        if split_position !=0:
            left_node = Node(node_to_split.text[:split_position], split_position, node_to_split)
            right_node = Node(node_to_split.text[split_position:], len(node_to_split.text)-split_position, node_to_split)
            node_to_split.left = left_node
            node_to_split.right = right_node
            node_to_split = node_to_split.right
        print(node_to_split)

    def printTree(self, node, level=0):
        if node != None:
            self.printTree(node.left, level + 1)
            print(' ' * 4 * level + '->', node.weight, node.text)
            self.printTree(node.right, level + 1)
