# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 09:17:26 2017
Exercise 4, version 1
@author: Luiza
"""

import unittest
import numpy as np

class Tile(object):

    '''Given (n by m) bool 2D array consisting of islands as True
    and water as False
    Counts the number of separate islands, that can be formed using 4-connectivity
    between the land tiles
    '''

    def __init__(self, bool_matrix, rows, cols):

        '''Initialization of tile as 2D numpy bool array (True/False or 0/1)
        checks whether we have the correct size and expects boolean array elements

        Args:
            bool_matrix: boolean numpy 2D array for tile
            rows, cols: size of the tile array
        '''

        (self.rows, self.cols) = np.shape(bool_matrix)
        if self.cols != cols or self.rows != rows:
            assert ValueError, "Given matrix dimensions mismatch between the actual size of array"
        self.tile = bool_matrix
        self.num_islands = 0
        self.unvisited_land_cells = set((i, j) for i in range(self.rows) \
        for j in range(self.cols) if self.tile[i, j])

    def is_unvisited_island(self, tuple_cell):

        """Checks if a given cell (x,y) is a land and was not visited so far

        Args:
            tuple_cell: a tuple (x,y) coordinate

        Returns:
            True: if not visited land
            False: otherwise
        """
        
        is_within_bounds = (0 <= tuple_cell[0] < self.rows and 0 <= tuple_cell[1] < self.cols)
        return is_within_bounds and ((tuple_cell[0], tuple_cell[1]) in self.unvisited_land_cells)


    def get_land_neighbours(self, cell):

        '''Returns a list of unvisited land tiles
        that can be riched from given cell (x,y)
        '''

        neighbour_cells = []

        for i, j in zip([-1, 0, 0, 1], [0, -1, 1, 0]):
            if self.is_unvisited_island((cell[0] + i, cell[1] + j)):
                neighbour_cells.append((cell[0] + i, cell[1] + j))
        return neighbour_cells

    def traverse_island(self, start_cell):

        '''Traverses all unvisited and connected land tiles from start_cell (x,y),
        works as DFS with O(self.rows x self.cols) time-complexity,
        since number of nodes is O(self.rows x self.cols) and
        vertices is max 4*self.rows x self.cols that is O(self.rows x self.cols)
        '''

        cells_to_visit = [start_cell]
        while cells_to_visit:
            cell = cells_to_visit.pop()
            self.unvisited_land_cells.discard(cell)
            cells_to_visit.extend(self.get_land_neighbours(cell))
        self.num_islands += 1

    def count_islands(self):

        while self.unvisited_land_cells:
            island_start = self.unvisited_land_cells.pop() #queue functionality
            self.traverse_island(island_start)
        return self.num_islands

class TestCountIslands(unittest.TestCase):

    def setUp(self):
        self.arr = np.array([[0, 1, 0, 1], [1, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0]])
        self.arr_no_land = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

        self.tile = Tile(self.arr, 4, 4)
        self.tile_no_land = Tile(self.arr_no_land, 4, 4)

    def test_wrong_dimension(self):
        self.assertRaises(Tile(self.arr, 4, 3))

    def test_count_islands(self):
        self.assertEqual(self.tile.count_islands(), 3)

    def test_zero_island(self):
        self.assertEqual(self.tile_no_land.count_islands(), 0)

if __name__ == '__main__':
    unittest.main()
