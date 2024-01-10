"""
Use this file to implement your solution for exercise 3-1 b.
"""
from exercise_1a import find_subtrees
import random


def replace_random_subtree(tree, symbol, subtrees):
    all_subtrees = find_subtrees(tree, symbol)
    if all_subtrees:
        target = random.choice(all_subtrees)
        replacement = random.choice(subtrees)
        return swap_subtree(tree, target, replacement)

def swap_subtree(tree, target_subtree, replacement_subtree):
    node, children = tree
    if tree == target_subtree:
        return replacement_subtree
    else:
        if children is not None:
            new_children = [swap_subtree(child, target_subtree, replacement_subtree) for child in children]
            return (node, new_children)
        else:
            return tree