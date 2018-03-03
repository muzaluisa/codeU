# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 09:06:26 2018
Lessons on "Writing Idiomatic Python"
by Jeff Knupp
@author: sayfu
"""

import numpy as np

def AllAdvices():
    
    x = 1
    y = 2
    z = 3
    
    # bad
    
    if x<=y and y<=z:
        print('Numbers are ordered')
    
    # good
    if x <= y <= z:
        print('Numbers are ordered')
        
    value = 'Development'    
        
    # bad
    my_person = False
    if value == 'Development' or value == 'Health':
        my_person = True     
    
    # good
    my_person = value in ('Development', 'Health')

    # bad
    flag_pos = False
    if x:
        flag_pos = True
    
    # good
    flag_pos = 1 if x else 0

    # using else with the loop if break was not caused
    # good
    a_list = [1, 2, 4]
    for a in a_list:
        if a < 0:
            print('Array is not strictly positive')
            break
    else:
        print('All the elements are positive')
        
    ''' using a function as values
    rather then creating separate functions
    '''
    
    action = 'Filter negative values'
    if action == 'Filter negative values':
        action_func = filter(lambda x: x > 0, a_list)
        
    if action == 'Take square root of the elements':
        action_func = map(lambda x: x^2, a_list)
    
    # fast swapping 2 values, instead of creating third variable
    x, y = y, x

    # using a chain of operations for the string
    str_ = ' Finland celebrates the independence this year'
    str_preprocessed = str_.strip().replace('Finland','Suomi')

    # using hashing of the string using ASCII codes
    hash_value = sum([ord(x) for x in str_preprocessed])

    # using all to determine if all elements in the list are true
    print('All elements are True?', all(a_list))


    # using the default parameter of dictionary using get
    profile = {'Name':'Luiza','Country':'Finland'}
    phone_num = profile.get('phone',-1)
    
    #using named tuples for working with db, with difficult data structures
    
    from collections import namedtuple
    profile = namedtuple('Profile',['Name','Country'])
    
    # using isinstance to determine the type of the object
    if isinstance(str_,str):
        return 1
    
    #using underscore for the functions used only within the class
    def _private_class_funcion():
        print('Please do not use me outside!')
        
    #using @property for setting the value of the variable automatically

    # defining repr function for machine readable output  in the class
    # in comparison __str__ used for human readable output
    def __repr__(a):
        print('a:', a)
        
    # using generator expressions instead of the list
    words = ['sasha','luiza']
    for w in (word.upper() for word in words):
        print(w)

    # using PEP 257 function documentation

    def sort_array(arr):

        '''Returns the sorted array in the assending order
        
        Arguments:
        arr -- an array of integer values
        '''

    # import a long list of modules with tuple to keep them together
    from sklearn import (metrics, feature_selection)

    # use sys.exit to return error codes

    if not words:
        sys.exit('Word list is empty')

              
if __name__ == '__main__':
    AllAdvices()
            
        
    
    
    