import logging
import unittest
import numpy as np
from RearrangeCarGroup8Movements import RearrangeCars

class TestRearrangeCars(unittest.TestCase):

    '''Unittests for RearrangeCars class and promised fuctionality
    '''

    def setUp(self):

        '''Basic setting that will be used in several tests
        '''
        self.init_order = [1, 2, 0, 3]
        self.final_order = [3, 1, 2, 0]
        self.rc = RearrangeCars(self.init_order, self.final_order)

    def test_rearrange_sample_cars(self):

        '''Tests on the toy example without special difficulties
        '''

        self.rc.rearrange_all_cars()
        self.assertEqual(self.rc.current_car_order, self.final_order)

    def test_rearrange_sample_cars_twice(self):

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
        rc_same.rearrange_all_cars()
        self.assertEqual(rc_same.current_car_order, self.final_order)

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
