
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:12:38 2017
CodeU exercise 1 refined second time
@author: Luiza
refined
"""

"""Task 1: Given 2 strings, decide if one of them is a permutation of the other
Return:
   1: if both strings are empty
   0: if one string is empty or they are not a permutation
   1: given trimmed  and lower-cased strings form a permutation
"""         

import numpy as np
import logging
import unittest
from collections import Counter
   
def is_permutation(str1,str2):
    str1 = str1.strip().lower()
    str2 = str2.strip().lower()
    if  not str1 and not str2:
        logging.warning("Two empty strings are permutations")
        return 1
    ord1 = [ord(a) for a in str1]
    ord2 = [ord(a) for a in str2]
    if np.prod(ord1)!=np.prod(ord2) or sum(ord1)!=sum(ord2) or len(ord1)!=len(ord2):
        return 0      
    else:
        if Counter(str1) == Counter(str2): 
            return 1
        else:
            return 0
            
  
class TestPermutation(unittest.TestCase):
    print 'Testing permutations..'
    def test_empty(self):
        self.assertTrue(is_permutation(" ","   "))
        self.assertFalse(is_permutation("permutation",""))

    def test_non_empty(self):
        self.assertTrue(is_permutation("permutation","tionpermuta"))
        self.assertTrue(is_permutation("*_","_*"))

      
# Task 2: Implement an algorithm to find the kth to last element of a singly linked list      
class Node:
    def __init__(self,value):
        self.val = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.N = 0
        self.tail = None

    def get_kth_last_element(self,k):
        if k > self.N-1:
            assert ValueError,'There are ' + str(self.N) + ' elements, k should be less than N'
        if not self.head:
            logging.warning('The list is empty')
            return None
        cur = self.head;
        for i in range(0,self.N-k-1):
            cur = cur.next
        return cur.val;    
            
    def insert(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            self.tail = self.head
            self.N+=1
            return  
        self.tail.next = new_node
        self.tail = new_node
        self.N+=1
        
    def print_list(self):
        if not self.head:
            logging.warning('Empty list')
        cur = self.head
        while cur:
            print cur.val,
            cur = cur.next 
        print '\n'
        return;  
   
class TestList(unittest.TestCase):
    def setUp(self):
       x = [0,1,2,3]
       self.ll = LinkedList()
       for a in x:
           self.ll.insert(a) 
       print '..Testing Single-Linked List'    
    def test_insert(self):   
        self.assertEqual(self.ll.N,4)
        
    def test_k_th_last_element(self):
        self.assertEqual(self.ll.get_kth_last_element(0),3)
        self.assertEqual(self.ll.get_kth_last_element(3),0)
        self.assertRaises(self.ll.get_kth_last_element(4))
            

if __name__ == '__main__':
    unittest.main() 
    
