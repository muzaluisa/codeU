# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 10:22:28 2017
Exercise set 2, Code U
@author: Luiza
"""
import logging
import unittest

class Tree():
    
    """Defines the class for the tree:
    self.children contains a dict of pairs (node:(left_child,right_child))
    self.head contains the value of the tree head
    None denotes the absence if the node
    """
    
    def __init__(self,children,head):
        self.children = children;
        self.head = head;

def dfs_path(tree_, start, end, path=None):

    """Yields all full paths from start node
    to end node, excluding the end node
    """
    
    tree = tree_.children
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex is None:
            continue
        for next in set(tree[vertex]) - set(path):
            if next == end:
                yield path
            else:
                stack.append((next, path+[next]))

def get_ancestors(tree_, node):

    """Returns the ancestors from head to a given node
    """

    head = tree_.head
    if not head:
        logging.warning('tree is empty, no ancestors')
        return None
    if head == node:
        logging.warning('Head has no ancestors')
        return None
    ancestors = list(dfs_path(tree_, head, node, path=None))
    if ancestors:
        return ancestors[0]
    else:
        assert ValueError, 'Node ' + str(node) + ' does not exist in the tree'

def get_least_common_ancestor(tree_, node1, node2):

    """Returns the least common ancestor
    for two given nodes
    """

    tree = tree_.children
    head = tree_.head
    if not tree:
        logging.warning('Common ancestor in empty tree is None')
        return None
    if node1 == node2:
        logging.warning('Nodes are the same, common ancestor is just a node parent')
        return get_ancestors(tree_, node1)[-1]
    if node1 == head or node2 == head:
        logging.warning('Common ancestor of nodes, one of which is node is None')
        return None
    parents1 = get_ancestors(tree_, node1)
    parents2 = get_ancestors(tree_, node2)
    min_length = min([len(parents1), len(parents2)])
    index_least_ancestor = [i for i in range(min_length) if parents1[i] == parents2[i]][-1]
    return parents1[index_least_ancestor]


class TestGetAncestors(unittest.TestCase):

    """Unittesting for get_ancestors function
    """

    def setUp(self):

        """Tree representation is a dictionary
        1st tuple value is left child node, second - right child node
        None means one of the child is missing
        Leaves of the tree have empty tuples
        Head of the tree is computed when needed using get_head() function
        """

        self.tree = Tree({16:(9, 18), 9:(3, 14), 3:(1, 5), 18:(None, 19), 19:(), 1:(), 5:(), 14:()},16)
        self.empty_tree = Tree({},None)

    def test_empty_tree(self):

        """Empty tree has None ancestors
        """

        self.assertEqual(get_ancestors(self.empty_tree, 19), None)

    def test_missing_node(self):

        """If one node is missing in tree, exception is raised
        """

        self.assertRaises(get_ancestors(self.tree, 6))

    def test_head_node(self):

        """The head node ancestor is None
        """

        self.assertEqual(get_ancestors(self.tree, 16), None)

    def test_other(self):

        """When tree is non-empty, node exists and not head
        """

        self.assertEqual(get_ancestors(self.tree, 18), [16])
        self.assertEqual(get_ancestors(self.tree, 14), [16, 9])
        self.assertEqual(get_ancestors(self.tree, 1), [16, 9, 3])
        
class TestGetLeastCommonAncestor(unittest.TestCase):

    """Unittesting for get_least_common_ancestor function
    """

    def setUp(self):

        """Initializing tree given as example in the assignment
        and second empty tree
        """

        self.tree = Tree({16:(9, 18), 9:(3, 14), 3:(1, 5), 18:(None, 19), 19:(), 1:(), 5:(), 14:()},16)
        self.empty_tree = Tree({},None)

    def test_empty_tree(self):

        """Testing empty tree, output should be None
        """

        self.assertEqual(get_least_common_ancestor(self.empty_tree, 19, 6), None)

    def test_missing_node(self):

        """Testing when one of nodes is missing, output should be None
        """

        self.assertRaises(get_least_common_ancestor(self.tree, 6, 16))

    def test_same_node(self):

        """Testing when both nodes are the same
        """

        self.assertEqual(get_least_common_ancestor(self.tree, 14, 14), 9)

    def test_head(self):

        """Testing one node is head
        """

        self.assertEqual(get_least_common_ancestor(self.tree, 16, 9), None)

    def test_other(self):

        """Testing all other cases
        """

        self.assertEqual(get_least_common_ancestor(self.tree, 1, 5), 3)
        self.assertEqual(get_least_common_ancestor(self.tree, 14, 5), 9)

if __name__ == '__main__':
    unittest.main()
    
