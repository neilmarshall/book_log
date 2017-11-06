#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 22:40:16 2017

@author: neilmarshall
"""

import unittest

from book_log.add_record import parse_command_line, validate_ISIN


class Test_parse_command_line(unittest.TestCase):

    def setUp(self):
        self.test_list = ['test title', 'test author',
                          'test ISIN', 'test genre']

    def test_valid_list_with_no_rating_parsed_correctly(self):
        self.assertTupleEqual(parse_command_line(self.test_list),
                              ('test title', 'test author', 'test ISIN',
                               'test genre', None))

    def test_valid_list_with_rating_parsed_correctly(self):
        self.test_list.append('4')
        self.assertTupleEqual(parse_command_line(self.test_list),
                              ('test title', 'test author', 'test ISIN',
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
    def test_invalid_list_with_invalid_ISIN(self):
        self.test_list[2] = 'an invalid ISIN'
        self.assertRaisesRegex(ValueError,
                               'ISIN not in correct format',
                               parse_command_line, self.test_list)


class Test_validate_ISIN(unittest.TestCase):

    @unittest.skip("'validate_ISIN' function not yet implemented")
    def test_validate_ISIN_returns_True_for_valid_ISIN(self):
        valid_ISIN = ''
        self.assertTrue(validate_ISIN(valid_ISIN))

    @unittest.skip("'validate_ISIN' function not yet implemented")
    def test_validate_ISIN_returns_False_for_invalid_ISIN(self):
        invalid_ISIN = ''
        self.assertFalse(validate_ISIN(invalid_ISIN))


if __name__ == '__main__':
    unittest.main()
