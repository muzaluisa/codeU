# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 10:37:40 2017
Rearrange the car assignment
@author: Luiza
"""

import logging
import unittest
import numpy as np

'''Given: There is a parking lot with N spaces and N-1 cars in it.
The parking lot is described by an array of numbers, that is a permutation of numbers
from 0 to N. Cars are with numbers from 1 to N-1, 0 means an empty parking space.

E.G. Initial order = [1, 2, 0, 3]
       Final order = [3, 1, 2, 0]

Task: to rearrange the cars in a given way
and print a series of moves from position x to y

For our example, the series of moves should be e.g.:
    move 1 to 2
    move 3 to 0
'''

class RearrangeCars(object):

    '''Class to rearrange the cars and print the moves
       - Uses car_position_dict to optimize searching the position of a given car
       - Stores additionally the position of empty spot in current car arrangement
       self.current_car_order.
       - Moves are either printed to the console or logged
       - Stores and updates min_num_steps_left that shows min number of moves left
        in order to avoid comparison current and final order lists that takes O(n)
    '''

    def __init__(self, init_car_order, final_car_order):

        '''Initializes class instance with initial, final order and
        stores the position of empty parking space in the current car order

        Arguments:
           init_car_order: a valid non-empty list of cars + 1 \
           empty_place given in their parking place order
           
           final_car_order: a valid non-empty list of cars + 1 \
           empty_place according to the desired order

        Returns:
            None
        '''

        self.initial_car_order = init_car_order
        self.current_car_order = init_car_order
        self.final_car_order = final_car_order
        self.empty_spot_position = self.current_car_order.index(0)
        self.print_console = True
        self.car_position_dict = {car:pos for pos, car in enumerate(init_car_order) \
                                  if car != 0} #search the index of car in O(1) via dict
        self.min_num_steps_left = None

    def print_one_step(self, from_idx):

        '''Prints a move of the car from position #from_idx to empty spot
        '''

        move_str = 'move from {0} to {1}'.format(from_idx, self.empty_spot_position)
        if self.print_console:
            print move_str
        else:
            logging.info(move_str)

    def create_log_file(self):

        '''In case the number of moves is more than 100
        writes the output to the logfile instead of the console
        '''

        logging.warning('Since the number of cars to arrange is {0} and more than 1000\
                        , the output with movements will be logged to the file\
                        '.format(len(self.initial_car_order)))
        logging.info('Initial car order:')
        logging.info(self.initial_car_order)
        logging.info('Final car order:')
        logging.info(self.final_car_order)
        logging.info('Moves:')

    def move_car_to_empty_slot(self, car_to_move_position):

        '''Arranges the car with car_to_move_position index to the empty slot
        Arguments:
            car_to_move_position: the position from where the car is moved
        Returns:
            None
        '''

        car_to_move = self.current_car_order[car_to_move_position]
        self.current_car_order[self.empty_spot_position] = car_to_move
        self.current_car_order[car_to_move_position] = 0

        self.car_position_dict[car_to_move] = self.empty_spot_position
        self.empty_spot_position = car_to_move_position

    def get_not_arranged_car_index(self):

        '''Finds first car index not yet standing on the final destination
        index should never reach the end since there should be at least
        one car not yet arranged
        '''

        index = 0
        while self.current_car_order[index] == self.final_car_order[index]:
            index += 1
            if index == self.empty_spot_position:
                index += 1

        return index

    def rearrange_one_car(self):

        '''Puts to the current empty space the car
        that should be on this place according to the final arrangement
        if current empty space position is different from the final order empty
        space position

        Otherwise picks up the random not arranged car and places it to the empty space
        '''

        if self.final_car_order[self.empty_spot_position] == 0:
            car_to_move_position = self.get_not_arranged_car_index()
            car_to_move = self.current_car_order[car_to_move_position]
        else:
            car_to_move = self.final_car_order[self.empty_spot_position]
            car_to_move_position = self.car_position_dict[car_to_move]
            self.min_num_steps_left -= 1

        self.print_one_step(car_to_move_position)
        self.move_car_to_empty_slot(car_to_move_position)

    def reset_variables_to_init_state(self):

        '''Resets variables to the same state when class was initialized
        Needed for running rearrange_all_cars function again
        '''

        self.current_car_order = self.initial_car_order
        self.empty_spot_position = self.current_car_order.index(0)
        self.car_position_dict = {car:pos for pos, car in \
                                  enumerate(self.initial_car_order) if car != 0}

    def get_min_num_moves(self):

        '''Returns the minumum number of moves
        to make final arrangement
        '''
        current_final_order_zipped = zip(self.current_car_order, self.final_car_order)
        num_arranged_cars = len([c1 for c1, c2 in current_final_order_zipped \
                                 if c1 == c2 and c1])
        min_steps_left = len(self.initial_car_order) - 1 - num_arranged_cars
        return min_steps_left

    def rearrange_all_cars(self):

        '''Rearranges all cars and prints the moves
        Note 1: In case there are more than 1000 moves to print
        logging into the file is done
        Note 2: Possible to run the function many times

        '''

        if self.initial_car_order == self.final_car_order:
            assert ValueError, 'Cars are already in the final order, \
            no moves are required'
        elif self.current_car_order == self.final_car_order:
            self.reset_variables_to_init_state()

        self.min_num_steps_left = self.get_min_num_moves()

        if self.min_num_steps_left > 1000:
            self.create_log_file()
            self.print_console = False

        while self.min_num_steps_left:
            self.rearrange_one_car()

class TestRearrangeCars(unittest.TestCase):

    '''Unittests for RearrangeCars class and promised fuctionality
    '''

    def setUp(self):

        '''Basic setting that will be used in several tests
        '''
        self.init_order = [1, 2, 0, 3]
        self.final_order = [3, 1, 2, 0]
        self.rc = RearrangeCars(self.init_order, self.final_order)

    def test_rearrange_all_cars(self):

        '''Tests on the toy example without special difficulties
        '''

        self.rc.rearrange_all_cars()
        self.assertEqual(self.rc.current_car_order, self.final_order)

    def test_rearrange_all_cars_twice(self):

        '''Test whether the class instance can properly handle
        running the same function twice
        '''

        self.rc.rearrange_all_cars()
        self.assertEqual(self.rc.current_car_order, self.final_order)
        self.rc.rearrange_all_cars()
        self.assertEqual(self.rc.current_car_order, self.final_order)

    def test_already_proper_order(self):

        '''Tests the case when initial and final orders are the same
        '''

        rc_same = RearrangeCars(self.final_order, self.final_order)
        self.assertRaises(rc_same.rearrange_all_cars())

    def test_same_empty_position(self):

        '''Tests the case when the position for the empty spot
        is the same in the initial and final setting
        '''

        final_order_same_empty = [3, 1, 0, 2]
        rc_same_empty_pos = RearrangeCars(self.init_order, final_order_same_empty)
        rc_same_empty_pos.rearrange_all_cars()
        self.assertEqual(rc_same_empty_pos.current_car_order, final_order_same_empty)

    def test_long_parking_lot(self):

        '''Runs 30 test case with different initial and final orders
        of length N to check that the final arrangement is correct
        '''

        num_spots = 1500
        for _ in range(30):
            init_order_long = list(np.random.permutation(num_spots))
            final_order_long = list(np.random.permutation(num_spots))
            rc_long = RearrangeCars(init_order_long, final_order_long)
            rc_long.rearrange_all_cars()
            self.assertEqual(rc_long.current_car_order, final_order_long)

if __name__ == '__main__':
    unittest.main()
