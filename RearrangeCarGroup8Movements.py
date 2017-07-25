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
        move_str = "Move car #%s from %s to %s" %(self.car, self.from_index, self.to_index)
        return move_str

    def print_log_file(self):
        move_str = "Move car #%s from %s to %s" %(self.car, self.from_index, self.to_index)
        logging.info(move_str)

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
        self.current_car_order = init_car_order
        self.final_car_order = final_car_order
        self.empty_spot_position = self.current_car_order.index(0)
        self.print_console = True
        self.car_position_dict = {car:pos for pos, car in enumerate(init_car_order) \
                                  if car} #search the index of car in O(1) via dict
        self.not_arranged_cars = {car for i, car in enumerate(init_car_order)\
                                  if init_car_order[i] != final_car_order[i] and car}

    def create_log_file(self):

        '''In case the number of moves is more than 1000
        writes the output to the logfile instead of the console
        '''
        
        num_cars = len(self.not_arranged_cars)
        info_message = 'Number of cars to arrange is {0} > 1000, movements are logged'.format(num_cars)
        logging_message = info_message
        logging.warning(logging_message)
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
        '''

        car = random.choice(tuple(self.not_arranged_cars)) # O(1)
        return self.car_position_dict[car]

    def rearrange_one_car(self):

        '''Puts to the current empty space the car
        that should be on this place according to the final arrangement
        if current empty space position is different from the final order empty
        space position

        Otherwise picks up the random not arranged car and places it to the empty space
        in this case the number of not arranged cars stays the same
        
        Complexity is O(1)
        '''

        if self.final_car_order[self.empty_spot_position] == 0:
            car_to_move_position = self.get_not_arranged_car_index()
            car_to_move = self.current_car_order[car_to_move_position]
        else:
            car_to_move = self.final_car_order[self.empty_spot_position]
            car_to_move_position = self.car_position_dict[car_to_move]
            self.not_arranged_cars.difference_update([car_to_move]) # O(1)


        movement = Movement(car_to_move, car_to_move_position, self.empty_spot_position)
        if self.print_console:
            print movement
        else:
            movement.print_log_file()

        self.move_car_to_empty_slot(car_to_move_position)

    def reset_variables_to_init_state(self):

        '''Resets variables to the same state when class was initialized
        Needed for running rearrange_all_cars function again
        '''

        self.current_car_order = self.initial_car_order
        self.empty_spot_position = self.current_car_order.index(0)
        self.car_position_dict = {car:pos for pos, car in \
                                  enumerate(self.initial_car_order) if car} # time O(n)
        self.not_arranged_cars = {car for i, car in enumerate(self.initial_car_order)\
                                  if self.initial_car_order[i] != self.final_car_order[i]\
                                  and car} # time O(n)

    def rearrange_all_cars(self):

        '''Rearranges all cars and prints the moves
        Note 1: In case there are more than 1000 moves to print
        logging into the file is done
        Note 2: Possible to run the function many times

        '''

        if self.initial_car_order == self.final_car_order:
            assert ValueError, 'Cars are already in the final order, no moves are required'
        elif self.current_car_order == self.final_car_order:
            self.reset_variables_to_init_state()

        if len(self.not_arranged_cars) > 1000:
            self.create_log_file()
            self.print_console = False

        '''Final solution is O(n)
        '''

        while self.not_arranged_cars:
            self.rearrange_one_car() # O(1)
            
