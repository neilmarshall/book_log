"""
Test module for add_record.py
"""

import datetime
import unittest

from book_log.add_record import parse_command_line, validate_ISBN


class Test_parse_command_line(unittest.TestCase):

    def setUp(self):
        self.test_list = ['test title', 'test author',
                          '0-201-53082-1', 'test genre']

    def test_valid_list_with_no_rating_or_date(self):
        self.assertTupleEqual(parse_command_line(self.test_list),
                              ('test title', 'test author', '0-201-53082-1',
                               'test genre', None, None))

    def test_valid_list_with_rating_but_no_date(self):
        self.test_list.append('4')
        self.assertTupleEqual(parse_command_line(self.test_list),
                              ('test title', 'test author', '0-201-53082-1',
                               'test genre', 4, None))

    def test_valid_list_with_date_but_no_rating_short_form(self):
        self.test_list.append('-D 10-12-2005')
        self.assertTupleEqual(parse_command_line(self.test_list),
                              ('test title', 'test author', '0-201-53082-1',
                               'test genre', None,
                               datetime.datetime(2005, 12, 10)))

    def test_valid_list_with_date_but_no_rating_long_form(self):
        self.test_list.extend(['--Date', '10-12-2005'])
        self.assertTupleEqual(parse_command_line(self.test_list),
                              ('test title', 'test author', '0-201-53082-1',
                               'test genre', None,
                               datetime.datetime(2005, 12, 10)))

    def test_valid_list_with_rating_and_date(self):
        self.test_list.extend(['4', '-D 10-12-2005'])
        self.assertTupleEqual(parse_command_line(self.test_list),
                              ('test title', 'test author', '0-201-53082-1',
                               'test genre', 4,
                               datetime.datetime(2005, 12, 10)))

    def test_invalid_list_with_rating_less_than_1(self):
        self.test_list.append('0')
        self.assertRaisesRegex(ValueError,
                               'Rating must be between 1 and 5, if present',
                               parse_command_line, self.test_list)

    def test_invalid_list_with_rating_more_than_5(self):
        self.test_list.append('6')
        self.assertRaisesRegex(ValueError,
                               'Rating must be between 1 and 5, if present',
                               parse_command_line, self.test_list)

    def test_invalid_list_with_invalid_ISBN(self):
        self.test_list[2] = 'an invalid ISBN'
        self.assertRaisesRegex(ValueError, 'ISBN not in correct format',
                               parse_command_line, self.test_list)


class Test_validate_ISBN(unittest.TestCase):

    def setUp(self):
        self.ISBN_10_digit = '0-201-53082-1'
        self.ISBN_13_digit = '978-0-306-40615-7'

    def test_10_digit_valid_ISBN_returns_True(self):
        self.assertTrue(validate_ISBN(self.ISBN_10_digit))

    def test_10_digit_invalid_ISBN_returns_False(self):
        for d in '023456789':
            with self.subTest(d=d):
                self.assertFalse(validate_ISBN(self.ISBN_10_digit[:-1] + d))

    def test_13_digit_valid_ISBN_returns_True(self):
        self.assertTrue(validate_ISBN(self.ISBN_13_digit))

    def test_13_digit_invalid_ISBN_returns_False(self):
        for d in '012345689':
            with self.subTest(d=d):
                self.assertFalse(validate_ISBN(self.ISBN_13_digit[:-1] + d))


if __name__ == '__main__':
    unittest.main()
