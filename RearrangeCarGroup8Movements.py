# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 10:37:40 2017
Rearrange the car assignment
Group 8 solution!
"""

import logging
import random

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

class Movement(object):

    """This class stores information about one movement,
    i.e. a car moving from position *from_index* to position *to_index*.
    """

    def __init__(self, car, from_index, to_index):
        self.car = car
        self.from_index = from_index
        self.to_index = to_index

    def __str__(self):
        move_str = "Move car #{0} from {1} to {2}".format(self.car, self.from_index, self.to_index)
        return move_str

class RearrangeCars(object):

    '''Class to rearrange the cars and print the moves
       - Uses car_position_dict to optimize searching the position of a given car
       - Stores additionally the position of empty spot in current car arrangement
       self.current_car_order.
       - Moves are either printed to the console or logged
       - Print moves in O(n), where n is the number of cars.
       - More precisely at most n + k moves are taken, where k << n is the amount of movements
       - where car is placed not to the final place
    '''

    def __init__(self, init_car_order, final_car_order):

        '''Initializes class instance with initial, final order and
        stores the position of empty parking space in the current car order
        Memory is O(n) to store 3 order lists, 1 car_position_dict and a set of
        not arranged cars

        Storing car_position_dict helps to search indices of car in O(1) instead of O(n)
        A set of not_arranged_cars helps to now when to stop in O(1) as well as to draw
        in O(1) unarranged car

        Arguments:
           init_car_order: a valid non-empty list of cars + 1 \
           empty_place given in their parking place order

           final_car_order: a valid non-empty list of cars + 1 \
           empty_place according to the desired order

        Returns:
            None
        '''

        self.initial_car_order = init_car_order
        self.final_car_order = final_car_order
        self.print_console = True
        self._variables_to_init_state()

    def print_moves_log_file(self, moves_list):

        '''Prints a list of moves to the log file

        Arguments:
            moves: a list of Movement class instances
        Returns:
            None
        '''

        info_message = 'Number moves is {N} > 1000, logging them..'.format(N=len(moves_list))
        print info_message
        logging.basicConfig(filename='RearrangeCarGroup8.log', filemode ='w', level=logging.DEBUG)
        logging.info('Initial car order: {init_order}'.format(init_order=self.initial_car_order))
        logging.info('Final car order: {final_order}'.format(final_order=self.final_car_order))
        logging.info('Moves:')
        for move in moves_list:
            logging.info(move.__str__())

    def print_moves_console(self, moves_list):

        '''Prints a list of moves
        Arguments:
            moves: a list of Movement class instances
        Returns:
            None
        '''

        print 'Initial car order: {init_order}'.format(init_order=self.initial_car_order)
        print 'Final car order: {final_order}'.format(final_order=self.final_car_order)
        print 'Moves: '

        for move in moves_list:
            if self.print_console:
                print move
            else:
                logging.info(move.__str__())
        print '\n'

    def _move_car_to_empty_slot(self, car_to_move_position):

        '''Arranges the car with car_to_move_position index to the empty slot
        Arguments:
            car_to_move_position: the position from where the car is moved
        Returns:
            None
        '''

        car_to_move = self.current_car_order[car_to_move_position]
        self.current_car_order[self.car_position_dict[0]] = car_to_move
        self.current_car_order[car_to_move_position] = 0

        self.car_position_dict[car_to_move] = self.car_position_dict[0]
        self.car_position_dict[0] = car_to_move_position

    def _get_not_arranged_car_index(self):

        '''Finds first car index not yet standing on the final destination
        '''

        car = random.choice(tuple(self.not_arranged_cars)) # O(1)
        return self.car_position_dict[car]

    def _rearrange_one_car(self):

        '''Puts to the current empty space the car
        that should be on this place according to the final arrangement
        if current empty space position is different from the final order empty
        space position

        Otherwise picks up the random not arranged car and places it to the empty space
        in this case the number of not arranged cars stays the same

        Complexity is O(1)
        '''

        if self.final_car_order[self.car_position_dict[0]] == 0:
            car_to_move_position = self._get_not_arranged_car_index()
            car_to_move = self.current_car_order[car_to_move_position]
        else:
            car_to_move = self.final_car_order[self.car_position_dict[0]]
            car_to_move_position = self.car_position_dict[car_to_move]
            self.not_arranged_cars.difference_update([car_to_move]) # O(1)

        self._move_car_to_empty_slot(car_to_move_position)
        return Movement(car_to_move, car_to_move_position, self.car_position_dict[0])

    def _variables_to_init_state(self):

        '''Resets variables to the same state when class was initialized
        Needed for running rearrange_all_cars function again
        '''

        self.current_car_order = self.initial_car_order
        self.car_position_dict = {car:pos for pos, car in \
                                  enumerate(self.initial_car_order)} # time O(n)
        self.not_arranged_cars = {car for i, car in enumerate(self.initial_car_order)\
                                  if self.initial_car_order[i] != self.final_car_order[i]\
                                  and car} # time O(n)

    def rearrange_all_cars(self):

        '''Rearranges all cars and prints the moves
        Note 1: In case there are more than 1000 moves to print
        logging into the file is done
        Note 2: Possible to run the function many times
        Final solution is O(n)
        '''
        
        self._variables_to_init_state()
        
        moves = []
        while self.not_arranged_cars:
            moves.append(self._rearrange_one_car()) # O(1)

        if len(moves) > 1000:
            self.print_moves_log_file(moves)
        else:
            self.print_moves_console(moves)
