#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 22:40:16 2017

@author: neilmarshall
"""

import unittest

from book_log.add_record import parse_command_line, validate_ISBN


class Test_parse_command_line(unittest.TestCase):

    def setUp(self):
        self.test_list = ['test title', 'test author',
                          'test ISBN', 'test genre']

    def test_valid_list_with_no_rating_parsed_correctly(self):
        self.assertTupleEqual(parse_command_line(self.test_list),
                              ('test title', 'test author', 'test ISBN',
                               'test genre', None))

    def test_valid_list_with_rating_parsed_correctly(self):
        self.test_list.append('4')
        self.assertTupleEqual(parse_command_line(self.test_list),
                              ('test title', 'test author', 'test ISBN',
                               'test genre', 4))

    def test_invalid_list_with_rating_less_than_1(self):
        self.test_list.append('0')
        self.assertRaisesRegex(ValueError,
                               'Rating must be between 1 and 5, if supplied',
                               parse_command_line, self.test_list)

    def test_invalid_list_with_rating_more_than_5(self):
        self.test_list.append('6')
        self.assertRaisesRegex(ValueError,
                               'Rating must be between 1 and 5, if supplied',
                               parse_command_line, self.test_list)

    @unittest.expectedFailure
    def test_invalid_list_with_invalid_ISBN(self):
        self.test_list[2] = 'an invalid ISBN'
        self.assertRaisesRegex(ValueError, 'ISBN not in correct format',
                               parse_command_line, self.test_list)


class Test_validate_ISBN(unittest.TestCase):

    def test_10_digit_valid_ISBN_returns_True(self):
        valid_ISBN = '0-201-53082-1'
        self.assertTrue(validate_ISBN(valid_ISBN))

    def test_13_digit_valid_ISBN_returns_True(self):
        valid_ISBN = '978-0-306-40615-7'
        self.assertTrue(validate_ISBN(valid_ISBN))

    @unittest.skip("Full range of negative scenarios not yet considered")
    def test_validate_ISBN_returns_False_for_invalid_ISBN(self):
        invalid_ISBN = ''
        self.assertFalse(validate_ISBN(invalid_ISBN))
