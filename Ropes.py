# node to store information in Ropes
class Node():
    weight = 0
    text = ""
    left = None
    right = None
    parent = None
    rweight = 0
    '''
    if node is leaf node the weight is length on text
    if notde is internal then weight is left subtree's leves sum
    '''
    def __init__(self, str1, size, par = None):
        self.weight = size
        self.text = str1
        self.parent = par
    
    def __str__(self):
        str1 = "Node Info { " + "text : "+ self.text + " weight: "+ str(self.weight) \
        + " rweight: "+str(self.rweight) + " }"
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
        root1, root2=self.split(self.root,0)
        print("Tree1")
        self.printTree(root1)
        print("Tree2")
        self.printTree(root2)

    
    def createRopes(self, str1, start, end, parent):
        node = Node("", -1)
        node.parent = parent
        if end - start > self.LEAF_SIZE:
            mid = start + (end - start)//2
            # node.weight = 
            node.left, sum1 = self.createRopes(str1, start, mid, node)
            node.right, sum2 = self.createRopes(str1, mid + 1, end, node)
            node.weight = sum1
            node.rweight = sum2
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
        new_node.rweight = self.getWeight(right_node)
        return new_node
    
    # still doublt if i needed this, since i have perent nodes
    def getWeight(self, node):
        if not node.left and not node.right:
            return node.weight
        return self.getWeight(node.left) + self.getWeight(node.right)  

    def split(self, node, index):
        # split corner case
        if index > node.weight + node.rweight:
            return None, node
        if index <= 1:
            return node, None
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
        # self.printTree(self.root)

        if split_position !=0:
            left_node = Node(node_to_split.text[:split_position], split_position, node_to_split)
            right_node = Node(node_to_split.text[split_position:], len(node_to_split.text)-split_position, node_to_split)
            node_to_split.left = left_node
            node_to_split.right = right_node
            node_to_split.text = ""
            node_to_split.weight = left_node.weight
            node_to_split.rweight = right_node.weight
            node_to_split = node_to_split.right
        list1 = []
        
        self.splitAndDelete(node_to_split, list1, index)
        new_part = self.constructTreeFromList(list1)
        return node, new_part

    def constructTreeFromList(self, list1):
        new_root = list1[0]
        for root in list1[1:]:
            new_root = self.concatenationOperation(new_root, root)
        return new_root

    def splitAndDelete(self, node, list1, index):
        k = 0
        list1.append(node)
        node = node.parent
        node.rweight = 0
        node.right = None
        while node:
            print(node)
            if node.right and (node.weight + node.right.weight + node.right.rweight)  >= index :
                list1.append(node.right)
                k += node.right.weight + node.right.rweight
                node.rweight = 0
                node.right = None
            if node.left:
                node.weight = node.left.weight + node.left.rweight
            if node.right:
                node.rweight = node.right.weight + node.right.rweight
            # if node.parent and node.parent.right != node:
            #     node.parent.weight -= k
            node = node.parent            


    def printTree(self, node, level=0):
        if node != None:
            self.printTree(node.left, level + 1)
            print(' ' * 4 * level + '->', node.weight, node.text)
            self.printTree(node.right, level + 1)
