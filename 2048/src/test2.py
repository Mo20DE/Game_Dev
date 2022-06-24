
# Python3 program to illustrate
# Expectimax Algorithm
  
# Structure to declare
# left and right nodes
class Node:
     
    def __init__(self, value):
         
        self.value = value
        self.left = None
        self.right = None
     
# Initializing Nodes to None
def newNode(v):
 
    temp = Node(v)
    return temp
 
# Getting expectimax
def expectimax(node, is_max):
 
    # Condition for Terminal node
    if (node.left == None and node.right == None):
        return node.value
     
    # Maximizer node. Chooses the max from the
    # left and right sub-trees
    if (is_max):
        return max(expectimax(node.left, False), expectimax(node.right, False))
  
    # Chance node. Returns the average of
    # the left and right sub-trees
    else:
        return (expectimax(node.left, True)+ expectimax(node.right, True))/2
     
# Driver code
if __name__=='__main__':
     
    # Non leaf nodes.
    # If search is limited
    # to a given depth,
    # their values are
    # taken as heuristic value.
    # But because the entire tree
    # is searched their
    # values don't matter
    root = newNode(0)
    root.left = newNode(0)
    root.right = newNode(0)
  
    # Assigning values to Leaf nodes
    root.left.left = newNode(10)
    root.left.right = newNode(10)
    root.right.left = newNode(9)
    root.right.right = newNode(100)
  
    res = expectimax(root, True)
    print("Expectimax value is "+str(res))