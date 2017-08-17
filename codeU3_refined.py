# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 09:17:26 2017
Exercise 3, version 2
@author: Luiza
"""

from collections import deque
import unittest
import numpy as np

class Dictionary(object):

    '''Stores lower-case vocabulary and all its prefixes as a set
    Two functions isWord and isPrefix are defined to check if given word/prefix is found
    '''

    def __init__(self, word_list):

        '''Initialization with a non-empty word-list
        prefixes are found automatically
        '''

        assert word_list, 'Please provide a non-empty list of words'
        word_list = [w.lower() for w in word_list if w]
        self.max_word_len = max(map(len, word_list))
        self.words = set(word_list)
        self.word_prefixes = set()
        for word in self.words:
            self.word_prefixes.update(self.getPrefixes(word))

    def getPrefixes(self, word):

        '''Returns the list of all prefixes of given word
        including the word itself
        '''
        
        return set([word[0:n] for n in range(1, len(word)+1)])

    def isWord(self, word):

        '''Returns whether the word presents in the vocabulary
        the function is case-invariant
        '''

        if not isinstance(word, str):
            assert TypeError, 'Input should be a string'
        return word.lower() in self.words

    def isPrefix(self, prefix):

        '''Returns whether the string is the prefix of one of the words in vocabulary
        the function is case-invariant
        '''

        if not isinstance(prefix, str):
            assert TypeError, 'Input should be a string'
        return prefix.lower() in self.word_prefixes

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

    def test_normal_input_isword(self):
        self.assertTrue(self.d.isWord('cats'))
        self.assertFalse(self.d.isWord('cat'))

    def test_normal_input_isprefix(self):
        self.assertTrue(self.d.isPrefix('car'))
        self.assertFalse(self.d.isPrefix('cs'))

class CharGrid(object):

    '''Given (n by m) grid of letters and a dictionary
    Return all possible words from dictionary that can be formed by traversing
    the grid cells without visiting the same cell twice
    '''

    def __init__(self, char_matrix, word_list):

        '''Initialization of char matrix as 2D numpy array
        checks whether we have a proper matrix and character values in it,
        saves them along with matrix shape as attributes and dictionary

        Args:
            char_matrix: char_matrix as 2D numpy
            word_list: a list of strings, dictionary
        '''

        char_array = char_matrix.flatten() # flattening for checking matrix shape correctness
        for c in char_array:
            if isinstance(c, list):
                assert TypeError, 'Please provide matrix type of data'
                return
            if not c.isalpha() or len(c) > 1:
                assert TypeError, 'Please provide grid values with only char entries'
                return
        self.grid = char_matrix
        self.dict = Dictionary(word_list)
        (self.m, self.n) = np.shape(char_matrix)

    def route_to_word(self, route):

        '''Finds a word, corresponding to the given route

        Args:
            route: a list of (x,y) indices

        Returns:
            word, corresponding to this route
            empty string if route is empty
        '''

        chars = [self.grid[x, y] for (x, y) in route]
        return ''.join(chars)

    def route_extend(self, route):

        '''Extends the route with 1 step into 8 possible directions

        Args:
            route: a list of (x,y) indices

        Returns:
            all possible routes where 1 step made in one of 8 directions
            each route is a list of tuple coordinates
        '''

        last_x = route[-1][0] #last route coordinate x
        last_y = route[-1][1] #last route coordinate y
        cells_set = set(route)
        route_extended = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j and i == 0:
                    continue
                if 0 <= last_x + i < self.m and 0 <= last_y + j < self.n\
                and (last_x + i, last_y + j) not in cells_set:
                    route_extended.append(route + [(last_x + i, last_y + j)])

        ''' old long alternative
        if last_x + 1 < self.m and (last_x + 1, last_y) not in cells_set: #ensure we don't visit the same cell twice
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
        '''

        return route_extended

    def search_words(self):

        '''Return all words found in the grid from a given dictionary
        Optimized by stopping searching longer route than maximum length of the dictionary word
        '''

        all_cells = [[(i, j)] for i in range(self.m) for j in range(self.n)]
        routes = deque(all_cells)
        words_found = set()
        while routes:
            route = routes.popleft() #queue functionality
            word = self.route_to_word(route)
            if self.dict.isPrefix(word):
                if self.dict.isWord(word):
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
