"""
Use this file to implement your solution for exercise 3-1 a.
"""

def find_subtrees(tree, symbol):
    subtrees = []
    node, children = tree
    if node == symbol:
        subtrees.append(tree)
    for child in children or []:
        subtrees.extend(find_subtrees(child, symbol))
    return subtrees