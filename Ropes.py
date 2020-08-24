# node to store information in Ropes
class Node():
    size = 0
    text = ""
    left = None
    right = None
    
    def __init__(self, str1, size):
        self.size = size
        self.text = str1

# main class to handle string manipulation
class Rope(object):
    LEAF_SIZE = 3
    root = None
    
    def __init__(self, document):
        self.root, sum1 = self.createRopes(document, 0, len(document) - 1)
        self.root1, sum1 = self.createRopes("document", 0, len("document") - 1)

        print("ggg")
        self.printTree(self.root)
        print(self.searchIndex(self.root, 10))
        self.printTree(self.concatenationOperation(self.root, self.root1))
    
    def createRopes(self, str1, start, end):
        node = Node("", -1)
        
        if end - start > self.LEAF_SIZE:
            mid = start + (end - start)//2
            # node.size = 
            node.left, sum1 = self.createRopes(str1, start, mid)
            node.right, sum2 = self.createRopes(str1, mid + 1, end)
            node.size = sum1
            return node, sum1 + sum2
        else:
            node.size = end - start + 1
            node.text = str1[start:end+1]
            return node, node.size

    def searchIndex(self, node, index):
        print(index, node.text)
        
        if node.size < index:
            return self.searchIndex(node.right, index - node.size)
        if not node.right and not node.left:
            return node.text[index-1]
        
        return self.searchIndex(node.left,  index)
    
    def concatenationOperation(self, root1, root2):
        new_node = Node("", -1)
        new_node.left = root1
        new_node.right = root2
        new_node.size = self.getWeight(root1)
        return new_node
    
    def getWeight(self, node):
        if not node.left and not node.right:
            return node.size
        return self.getWeight(node.left) + self.getWeight(node.right)  

    def printTree(self, node, level=0):
        if node != None:
            self.printTree(node.left, level + 1)
            print(' ' * 4 * level + '->', node.size, node.text)
            self.printTree(node.right, level + 1)
