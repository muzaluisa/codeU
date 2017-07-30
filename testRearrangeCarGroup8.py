import unittest
import numpy as np
from RearrangeCarGroup8 import RearrangeCars

class TestRearrangeCars(unittest.TestCase):

    '''Unittests for RearrangeCars class and promised fuctionality
    '''

    def setUp(self):

        '''Basic setting that will be used in several tests
        '''
        
        self.initial_car_order = [1, 2, 0, 3]
        self.final_car_order = [3, 1, 2, 0]
        self.rc = RearrangeCars(list(self.initial_car_order), list(self.final_car_order))

    def test_empty_parking_lot(self):

        '''Test the case when the parking lot is empty,
        should work without raising an error
        '''
        
        rc_empty = RearrangeCars([], [])
        rc_empty.rearrange_all_cars(print_console=True)
        self.assertEqual(rc_empty.current_car_order, [])

    def test_parking_lot_length_one(self):

        '''Test the case when the parking lot is of
        length one and there is no car placed in it
        '''
        
        rc_length_one = RearrangeCars([0], [0])
        rc_length_one.rearrange_all_cars(print_console=True)
        self.assertEqual(rc_length_one.current_car_order, [0])

    def test_rearrange_sample_cars(self):

        '''Tests on the toy example without special difficulties
        '''

        self.rc.rearrange_all_cars(print_console=True)
        self.assertEqual(self.rc.current_car_order, self.final_car_order)

    def test_initial_order_preserved(self):

        '''Tests whether, after having called rearrange_all_cars() once,
        the field self.initial_car_order is still unchanged

        Note: This test must pass for test_rearrange_sample_cars_twice to
        be meaningful
        '''
        self.rc.rearrange_all_cars(print_console=True)
        self.assertEqual(self.rc.initial_car_order, self.initial_car_order)

    def test_rearrange_sample_cars_twice(self):

        '''Test whether the class instance can properly handle
        running the same function twice
        '''

        self.rc.rearrange_all_cars(print_console=True)
        self.assertEqual(self.rc.current_car_order, self.final_car_order)
        self.rc.rearrange_all_cars(print_console=True)
        self.assertEqual(self.rc.current_car_order, self.final_car_order)

    def test_already_proper_order(self):

        '''Tests the case when initial and final orders are the same
        '''

        rc_same = RearrangeCars(self.final_car_order, self.final_car_order)
        rc_same.rearrange_all_cars(print_console=True)
        self.assertEqual(rc_same.current_car_order, self.final_car_order)

    def test_same_empty_position(self):

        '''Tests the case when the position for the empty spot
        is the same in the initial and final setting
        '''

        final_order_same_empty = [3, 1, 0, 2]
        rc_same_empty_pos = RearrangeCars(self.initial_car_order, final_order_same_empty)
        rc_same_empty_pos.rearrange_all_cars(print_console=True)
        self.assertEqual(rc_same_empty_pos.current_car_order, final_order_same_empty)

    def test_parking_lot_different_length_value_error(self):

        '''Tests the case when initial_car_order and final_car_order
        given are of different length
        A ValueError shall raise
        '''

        final_car_order_different_length = [0, 1, 2, 3, 4]
        rc_parking_lot_different_length = RearrangeCars(self.initial_car_order,
                                                        final_car_order_different_length)
        with self.assertRaises(ValueError):
            rc_parking_lot_different_length.rearrange_all_cars(print_console=True)

    def test_long_parking_lot(self):

        '''Runs 30 test case with different initial and final orders
        of length num_spots to check that the final arrangement is correct
        as well as logging function
        '''

        num_spots = 1500
        for _ in range(30):
            init_order_long = list(np.random.permutation(num_spots))
            final_order_long = list(np.random.permutation(num_spots))
            rc_long = RearrangeCars(init_order_long, final_order_long)
            rc_long.rearrange_all_cars()
            self.assertEqual(rc_long.current_car_order, final_order_long)

if __name__ == '__main__':
    unittest.main(verbosity=2)
