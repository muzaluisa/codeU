# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 09:17:26 2017
Exercise 3, version 1
@author: Luiza
"""

from collections import deque
import unittest
import numpy as np

def find_prefixes(word):

    '''Returns the list of prefixes of given word
    including the word itself
    '''

    return set([word[0:n] for n in range(1, len(word)+1)])

class Dictionary(object):

    '''Stores lower-case vocabulary and all its prefixes
    '''

    def __init__(self, word_list):
        if not word_list:
            assert ValueError, 'Please provide non-empty list of words'
        word_list = [w.lower() for w in word_list if w]
        self.max_word_len = reduce(max, map(len, word_list))
        self.words = set(word_list)
        self.word_prefixes = set()
        for word in self.words:
            self.word_prefixes.update(find_prefixes(word))

    def isWord(self, word):

        '''Returns whether the word presents in the vocabulary
        the function is case-invariant
        '''

        if not isinstance(word, str):
            assert TypeError, 'Input should be a string'
            return
        if word.lower() in self.words:
            return True
        return False

    def isPrefix(self, prefix):

        '''Returns whether the string is the prefix of one of the words in vocabulary
        the function is case-invariant
        '''

        if not isinstance(prefix, str):
            assert TypeError, 'Input should be a string'
            return
        if prefix.lower() in self.word_prefixes:
            return True
        return False

class TestDictionary(unittest.TestCase):

    '''Testing dictionary basic functions
    '''

    def setUp(self):
        self.d = Dictionary(['cats', 'dogs', 'cars', ' ', ''])

    def test_empty_input(self):
        self.assertFalse(self.d.isWord('  '))
        self.assertFalse(self.d.isPrefix(''))

    def test_case(self):
        self.assertTrue(self.d.isWord('Cats'))
        self.assertTrue(self.d.isPrefix('DOGS'))

    def test_normal_input(self):
        self.assertTrue(self.d.isWord('cats'))
        self.assertTrue(self.d.isPrefix('car'))

        self.assertFalse(self.d.isWord('cat'))
        self.assertFalse(self.d.isPrefix('cs'))

    def test_nonstring_input(self):
        self.assertRaises(self.d.isWord(['cat', 'cats']))
        self.assertRaises(self.d.isPrefix(['cat', 'cats']))

class CharGrid(object):

    '''Given(n by m) grid of letters and a dictionary
    Return all possible words from dictionary that can be formed by traversing
    the grid cells without visiting the same cell twice
    '''

    def __init__(self, char_arr, words):
        char_arr_fl = char_arr.flatten()
        for c in char_arr_fl:
            if isinstance(c, list):
                assert TypeError, 'Please provide matrix type of data'
                return
            if not c.isalpha() or len(c) > 1:
                assert TypeError, 'Please provide grid values with only char entries'
                return
        self.grid = char_arr
        self.dict = Dictionary(words)
        (self.m, self.n) = np.shape(char_arr)

    def is_route_prefix(self, route):

        '''Given a list of tuple coordinates (x,y) encoding route
        Returns True if route gives string that is a prefix in our dictionary
        '''

        if not route:
            return False
        chars = [self.grid[x, y] for (x, y) in route]
        prefix = ''.join(chars)
        if self.dict.isPrefix(prefix):
            return True
        return False

    def route_word(self, route):

        '''Given a list of tuple coordinates (x,y) encoding route
        Returns empty string if corresponding string is not in the dictionary
        and word otherwise
        '''

        if not route:
            return ""
        chars = [self.grid[x, y] for (x, y) in route]
        word = ''.join(chars)
        if self.dict.isWord(word):
            return word
        return ""

    def route_extend(self, route):

        '''Given a route as list of (x,y) indices
        Returns all possible routes 1 step made in one of 8 directions
        '''

        last_x = route[-1][0] #last route coordinate x
        last_y = route[-1][1] #last route coordinate y
        cells_set = set(route)
        route_extended = []

        if last_x + 1 < self.m and (last_x + 1, last_y) not in cells_set:
            route_extended.append(route + [(last_x + 1, last_y)])
        if last_x + 1 < self.m and last_y + 1 < self.n and (last_x + 1, last_y + 1) not in cells_set:
            route_extended.append(route + [(last_x + 1, last_y + 1)])
        if last_y + 1 < self.n and (last_x, last_y + 1) not in cells_set:
            route_extended.append(route + [(last_x, last_y + 1)])
        if last_x - 1 >= 0 and (last_x - 1, last_y) not in cells_set:
            route_extended.append(route + [(last_x - 1, last_y)])
        if last_x - 1 >= 0 and last_y + 1 < self.n and (last_x - 1, last_y + 1) not in cells_set:
            route_extended.append(route+[(last_x - 1, last_y + 1)])
        if last_x - 1 >= 0 and last_y - 1 >= 0 and (last_x - 1, last_y - 1) not in cells_set:
            route_extended.append(route + [(last_x - 1, last_y - 1)])
        if last_y - 1 >= 0 and (last_x, last_y - 1) not in cells_set:
            route_extended.append(route + [(last_x, last_y - 1)])
        if  last_x + 1 < self.m and last_y - 1 >= 0 and (last_x + 1, last_y - 1) not in cells_set:
            route_extended.append(route + [(last_x + 1, last_y - 1)])

        return route_extended

    def search_words(self):

        '''Return all words found in the grid from given dictionary
        '''

        all_cells = [[(i, j)] for i in range(self.m) for j in range(self.n)]
        routes = deque(all_cells)
        words_found = set()
        while routes:
            route = routes.popleft()
            if self.is_route_prefix(route):
                word = self.route_word(route)
                if word:
                    words_found.add(str(word))
                if len(route) < self.dict.max_word_len:
                    routes.extendleft(self.route_extend(route))
        return words_found

class TestCharGrid(unittest.TestCase):

    '''Unit tests to check word search in the grid
    '''

    def setUp(self):
        self.d = Dictionary(['cats', 'dogs', 'cars', ' ', ''])
        self.charGrid = CharGrid(np.array([['a', 'a', 'r'], ['t', 'c', 'd']]),\
                                 ['CAR', 'CARD', 'CART', 'CAT'])

    def test_non_char_entry(self):
        self.assertRaises(CharGrid(np.array([['a', '2', 'r'], ['t', 'c', 'd']]),\
                                   ['CAR', 'CARD', 'CART', 'CAT']))

    def test_non_matrix_entry(self):
        self.assertRaises(CharGrid(np.array([['a', '2'], ['t', 'c', 'd']]),\
                                   ['CAR', 'CARD', 'CART', 'CAT']))

    def test_normal_input(self):
        self.assertEqual(self.charGrid.search_words(), set(['car', 'card', 'cat']))


if __name__ == '__main__':
    unittest.main()
