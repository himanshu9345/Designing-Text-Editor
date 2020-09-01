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
        + " rweight: "+str(self.rweight) + " left: "+str(self.left)+ " }"
        return str1



# main class to handle string manipulation
class Rope(object):
    LEAF_SIZE = 3
    # root
    # def __init__(self,document):
        # self.root, sum1 = self.createRopes(document, 0, len(document) - 1, None)
        # self.root1, sum1 = self.createRopes("document", 0, len("document") - 1, None)

    #     # print("ggg")
        # self.printTree(self.root)
        # self.reportOperation(self.root )
    #     # print(self.searchIndex(self.root, 10))
    #     # self.printTree(self.concatenationOperation(self.root, self.root1))
        # root1, root2=self.split(self.root,4)
        # print("Tree1")
        # self.printTree(root1)
        # print("Tree2")
        # self.printTree(root2)

        # self.deleteText(self.root, 2,9)

    
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
            node.weight = end - start +1
            node.text = str1[start-1:end]
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
        if not left_node:
            return right_node
        if not right_node:
            return left_node
        new_node = Node("", -1)
        new_node.left = left_node
        new_node.right = right_node
        left_node.parent = new_node
        right_node.parent = new_node
        new_node.weight = left_node.weight + left_node.rweight
        new_node.rweight = right_node.weight + right_node.rweight
        return new_node
    
    # still doublt if i needed this, since i have perent nodes
    def getWeight(self, node):
        if not node.left and not node.right:
            return node.weight
        return self.getWeight(node.left) + self.getWeight(node.right)  

    def split(self, node, index):
        # print(node,  "inside split")
        # split corner case
        if index > node.weight + node.rweight:
            return None, node
        if index <= 1:
            return  None, node
        node_to_split, split_position = self.searchIndexReturnNode(node, index)
        # print("to split", node_to_split, split_position,index)
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
            node_to_split.weight = left_node.weight + left_node.rweight
            node_to_split.rweight = right_node.weight + right_node.rweight
            node_to_split = node_to_split.right
        
        # print(node_to_split)
        last_visited = None
        sum_broken_weight = 0
        self.curr_merge_tree = None
        self.fun1(node_to_split, last_visited, sum_broken_weight)
        # if root_val > index:
        #     self.splitAndDelete(node_to_split, list1, index)
        # else:

        # new_part = self.constructTreeFromList(list1)
        return node, self.curr_merge_tree

    def fun1(self, node_curr, last_visited, sub_w):
        if not last_visited:
            # print("leaf node", node_curr)
            sub_w += node_curr.weight
            if node_curr.parent:
                curr_parent = node_curr.parent
                node_curr.parent.right = None
                node_curr.parent = None 
                self.curr_merge_tree = node_curr
                self.fun1(curr_parent, node_curr, sub_w)

            
        else:
            # print("if statement")
            # print(node_curr)
            # print(last_visited)
            if node_curr.left == last_visited:
                broken = node_curr.right
                if broken:
                    node_curr.right.parent = None
                    node_curr.right = None
                node_curr.weight -= sub_w
                sub_w += node_curr.rweight
                node_curr.rweight = 0
                self.curr_merge_tree=self.concatenationOperation(self.curr_merge_tree, broken)	
                # print("left node self.curr_merge_tree", node_curr)
                # self.printTree(self.curr_merge_tree)
            else:
                node_curr.rweight -= sub_w
                # print("right node self.curr_merge_tree",node_curr)
                # self.printTree(self.curr_merge_tree)

            last_visited = node_curr
            node_curr= node_curr.parent
            # print("node curr",node_curr)
            # print("last visited",last_visited)

            if not node_curr:
                return
            self.fun1(node_curr, last_visited, sub_w)

    def constructTreeFromList(self, list1):
        # print("inside construct")
        new_root = list1[0]
        # print(new_root)
        for root in list1[1:]:
            # print(root)
            new_root = self.concatenationOperation(new_root, root)
        
        # print("going out construct")
        
        return new_root

    def splitAndDelete(self, node, list1, index):
        k = 0
        list1.append(node)
        # print("in split and del", node)
        node = node.parent
        node.rweight = 0
        node.right = None
        while node:
            print(node)
            if node.right and (node.weight + node.right.weight + node.right.rweight)  >= index :
                list1.append(node.right)
                # print(list1[-1],"to move")
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
        # print("out of split and del")
    
    def splitAndDeleteRight(self, node, list1, index):
        k = 0
        list1.append(node)
        # print("in split and del", node)
        node = node.parent
        node.rweight = 0
        node.right = None
        while node:
            # print(node)
            if node.right and (node.weight + node.right.weight + node.right.rweight)  >= index :
                list1.append(node.right)
                # print(list1[-1],"to move")
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
        # print("out of split and del")
               

    def deleteText(self, node, i, j):
        '''
        Assumption 
        - i < j
        - if i < 1 then i will become 1

        input parameter (node, i, j)
        i,j -> 1 index based
        **************************************
        return (new node(rope), deleted rope) 
        **************************************
        '''
        if i<1:
            i = 1
        # self.printTree(node)
        # print(i,j, node)
        merged_node = None
        node_to_concat1, node_to_del1 = self.split(node, i)
        # self.printTree(node_to_del1)
        # print("ffffffffgggggggggggggggggggggggggggggggg")
        # self.printTree(node_to_concat1)
        node_to_del2, node_to_concat2 = self.split(node_to_del1, j - i +1 )
        # print("node_to_concat2", j-i+1)
        # self.printTree(node_to_concat2)
        if node_to_concat1 and node_to_concat2:
            merged_node = self.concatenationOperation(node_to_concat1, node_to_concat2)
        elif node_to_concat1:
            merged_node = node_to_concat1
        elif node_to_concat2:
            merged_node = node_to_concat2
        # merged_deleted_node = self.concatenationOperation(node_to_concat1, node_to_concat2)
        # print("new node")
        # self.printTree(merged_node)
        # print("node to del")
        # self.printTree(node_to_del2)
        return merged_node, node_to_del2

    def reportOperation(self, node, i = 1, j = float('inf')):
        '''
        find the node with ith charcater(1 indexed)
        then do inorder traversal using parent, right and left
        '''
        if not node:
            return ""
        # self.printTree(node)
        u_th_node , idx = self.searchIndexReturnNode(node, i)

        str_final = u_th_node.text[idx:]
        i += len(u_th_node.text[idx:])
        stack = [u_th_node]
        root = u_th_node.parent
        diff = j - i 
        # print(u_th_node, i, j, diff)

        while root and diff:
            if root.right:
                # print(root.right,"gg")
                str1, d= self.inorderTraversal(root.right, diff)
                str_final+=str1
                diff = d
            # if not root.par
            root = root.parent
            # print(str_final, str1, root, diff, d)
        return str_final


    def inorderTraversal(self, root, diff):
        str1 = ""
        stack = []
        while diff>0 and (root or stack):
            while root:
                stack.append(root)
                root = root.left
            root = stack.pop()
            str1 += root.text[:min(diff, len(root.text))]
            diff -= min(diff, len(root.text))
            root = root.right
        return str1, diff

        




    def printTree(self, node, level=0):
        if node != None:
            self.printTree(node.left, level + 1)
            print(' ' * 4 * level + '->', node.weight, node.text)
            self.printTree(node.right, level + 1)
