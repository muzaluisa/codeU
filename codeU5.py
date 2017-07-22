# -*- coding: utf-8 -*-
# Revised 1st version

from collections import defaultdict
import numpy as np
import unittest

'''Given a dictionary (a list of words in lexicographic order) of all words in an unknown/invented
language, find the alphabet (an ordered list of characters) of that language.
This language can contain any character (of the native char data type). Upper/lower case
characters are treated differently for simplicity. Assume standard lexicographical ordering
(order by characters from left to right, if X is a prefix of Y then X is sorted before Y), just with
an unknown order of characters.
Write a function that will receive an ordered list of strings, and returns an ordered list of
characters'''

class Alphabet:
    def __init__(self,word_list):
        
        '''Args:
            word_list: non-empty list of unique words from the given language
        '''
        
        self.words = word_list
        self.partial_order = set() # a list of partial order lists [char1,char2], char1 < char2
        self.all_chars = set() # unordered set of all characters
        self.sorted_alphabet = [] # the list of characters in the alphabetical order
        for word in self.words:
            self.all_chars.update(set(word))
        self.unmarked = self.all_chars # used in top-sort, nodes which order is not yet determinded
        self.temp_marked = set() # used in top-sort for marking visited nodes
        
        self.neigh_dict = defaultdict(list) # dictionary of char: [list of chars going after the given char] 
        
    def find_common_prefix(self, word1, word2):

        prefix = ''    
        for c1, c2 in zip(word1,word2):
            if c1 != c2:
                return prefix
            else:
                prefix+=c1
    
    def find_partial_order(self, word1, word2):
        
        '''Returns:
            partial order [char_prev,char_next]
            inferred from two words word1 and word2
        '''
        
        prefix = self.find_common_prefix(word1, word2)
        char_first = word1[len(prefix)]
        char_next = word2[len(prefix)]
        return (char_first, char_next)
    
    def find_all_partial_orders(self):
        
        '''Returns:
            all partial orders inferred from
            each subsequent pair of words
        '''
        
        for i in range(len(self.words) - 1):
            # if one word is contained in the other, then we can not infer the partial order
            if self.words[i] in self.words[i+1] or self.words[i+1] in self.words[i]:
                continue    
            char_prev, char_next = self.find_partial_order(self.words[i], self.words[i+1])
            self.partial_order.add((char_prev, char_next))
            
        for char_prev, char_next in self.partial_order:
            if char_prev not in self.neigh_dict:
                self.neigh_dict[char_prev] = [char_next]
            else:
                self.neigh_dict[char_prev]+= [char_next] 
                
        return self.partial_order 
    
    def topological_sort(self):
        
        '''The implementation of topological sort
        based on DFS, check https://en.wikipedia.org/wiki/Topological_sorting
        Returns:
            sorted alphabet 
        '''
        self.partial_order = set()
        self.neigh_dict = defaultdict(list)
        self.find_all_partial_orders()
        for node in self.unmarked.copy():
            self.visit_node(node)
        return self.sorted_alphabet    
            
    def visit_node(self, node):
        assert node not in self.temp_marked, "Provided order of words is wrong, character " \
            + str(node) + " order can not be determined correctly! "
        
        #assert node in self.temp_marked, 
        if node not in self.unmarked:
            return
        self.temp_marked.add(node)
        for neigh_node in self.neigh_dict[node]:
            self.visit_node(neigh_node)
        self.unmarked.remove(node)
        self.temp_marked.remove(node)
        self.sorted_alphabet.insert(0, node)
   
class TestAlphabet(unittest.TestCase):

    def setUp(self):
        word_list = ['ART', 'RAT', 'CAT', 'CAR']
        self.a = Alphabet(word_list)

    def test_partial_order(self):
        partial_order_set = self.a.find_all_partial_orders()
        self.assertEqual(partial_order_set, {('A', 'R'), ('R', 'C'), ('T', 'R')})

    def test_alphabet_order(self):
        right_answer1 = ['T', 'A', 'R', 'C']
        right_answer2 = ['A', 'T', 'R', 'C']
        answer = self.a.topological_sort()
        self.assertTrue(answer == right_answer1 or answer == right_answer2)

if __name__ == '__main__':
    unittest.main()    
