# -*- coding: utf-8 -*-
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
        self.partial_order = [] # a list of partial order lists [char1,char2], char1 < char2
        self.all_chars = set() # unordered set of all characters
        self.sorted_alphabet = [] # the list of characters in the alphabetical order
        for word in self.words:
            self.all_chars.update(set(word))
        self.neigh_dict = defaultdict(list) # dictionary of char: [list of chars going after the given char] 
        
    def find_common_prefix(self, word1, word2):
        
        if len(word1) < len(word2):
            word_shorter = word1
            word_longer = word2
        else:
            word_longer = word1
            word_shorter = word2
            
        for i, c in enumerate(word_shorter):
            if c != word_longer[i]:
                return word_shorter[:i]
    
    def find_partial_order(self, word1, word2):
        
        '''Returns:
            partial order [char_prev,char_next]
            inferred from two words word1 and word2
        '''
        
        prefix = self.find_common_prefix(word1, word2)
        char_first = word1[len(prefix)]
        char_next = word2[len(prefix)]
        return [char_first, char_next]
    
    def find_all_partial_orders(self):
        
        '''Returns:
            all partial orders inferred from
            each subsequent pair of words
        '''
        
        for i in range(len(self.words) - 1):
            # if one word is contained in the other, then we can not infer the partial order
            if self.words[i] in self.words[i+1] or self.words[i+1] in self.words[i]:
                continue    
            [char_prev, char_next] = self.find_partial_order(self.words[i], self.words[i+1])
            self.partial_order.append([char_prev, char_next])
        return self.partial_order 
    
    def find_neighbours(self):
        
        '''Creates a dictionary 
        with key as a char and value being as a list of chars
        that go next in the alphabetical order
        '''
        
        for [char_prev, char_next] in self.partial_order:
            if char_prev not in self.neigh_dict:
                self.neigh_dict[char_prev] = [char_next]
            else:
                self.neigh_dict[char_prev]+= [char_next]
    
    def topological_sort(self):
        
        '''The implementation of topological sort
        based on DFS, check https://en.wikipedia.org/wiki/Topological_sorting
        Returns:
            sorted alphabet 
        '''
        
        self.find_all_partial_orders()
        self.find_neighbours()
        self.temp_marked = set()
        self.unmarked = self.all_chars
        unmarked = self.unmarked.copy()
        for node in unmarked:
            self.visit_node(node)
        return self.sorted_alphabet    
            
    def visit_node(self,node):
        if node not in self.unmarked:
            return
        self.temp_marked.add(node)
        for neigh_node in self.neigh_dict[node]:
            self.visit_node(neigh_node)
        self.unmarked.remove(node)
        self.temp_marked.remove(node)
        self.sorted_alphabet.insert(0, node)
   
class TestAlhabet(unittest.TestCase):

    def setUp(self):
        word_list = ['ART', 'RAT', 'CAT', 'CAR']
        self.a = Alphabet(word_list)

    def test_partial_order(self):
        partial_order_list = self.a.find_all_partial_orders()
        self.assertEqual(partial_order_list, [['A', 'R'], ['R', 'C'], ['T', 'R']])

    def test_alphabet_order(self):
        right_answer1 = ['T', 'A', 'R', 'C']
        right_answer2 = ['A', 'T', 'R', 'C']
        answer = self.a.topological_sort()
        self.assertTrue(answer == right_answer1 or answer == right_answer2)

if __name__ == '__main__':
    unittest.main()    
