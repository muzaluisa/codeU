# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:12:38 2017
CodeU exercise 1
@author: Luiza
"""

# Task 1: Given 2 strings, decide if one of them is a permutation of the other
# Return:
#         1: if both strings are empty
#         0: if one string is empty or they are not a permutation
#         1: given trimmed strings form a permutation

import numpy as np
   
def is_permutation(str1,str2):
    yes = "'" + str1 + "'" + " is a permutation of " + "'" + str2 + "'";
    no = "'" + str1 + "'" + " is not a permutation of " + "'" + str2 + "'";
    str1 = str1.strip().lower()
    str2 = str2.strip().lower()
    if  not str1 and not str2:
        print "Two empty strings are permutations"
        return 1
    ord1 = [ord(a) for a in str1]
    ord2 = [ord(a) for a in str2]
    if np.prod(ord1)!=np.prod(ord2):
        print no
        return 0;     
    if sum(ord1)!=sum(ord2):
        print no
        return 0;      
    else:
        print yes
        return 1;
        
    
is_permutation("permutation","")
is_permutation("permutation","tionpermuta")
is_permutation("_*","*_")
is_permutation("  ","  ")

 # Tast 2: Implement an algorithm to find the kth to last element of a singly linked list  
   
      
class Node:
    def __init__(self,value):
        self.val = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None;
        self.N = 0

    def k_last(self,k):
        if k > self.N-1:
            print 'There are ' + str(self.N) + ' elements, k should be less than N';
            return None;
        if not self.head:
            print 'The list is empty';
            return None;
        cur = self.head;
        for i in range(0,self.N-k-1):
            cur = cur.next
        return cur.val;    
            
    def insert(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node;
            self.N = self.N+1;
            return;
        cur = self.head
        while cur.next:
            cur = cur.next   
        cur.next = new_node 
        self.N = self.N+1;
        
    def print_list(self):
        if not self.head:
            print 'Empty list'
        cur = self.head
        while cur:
            print cur.val,
            cur = cur.next 
        print '\n'
        return;    
        
def k_last_element(x,k):
    print str(k) + 'th last element is ' + str(ll.k_last(k))     

x = [0,1,2,3]
ll = LinkedList();
for a in x:
    ll.insert(a)
print '\nList:'
ll.print_list()
    
k_last_element(ll,0)
k_last_element(ll,1)
k_last_element(ll,4)
    