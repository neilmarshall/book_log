"""
Test module for add_record.py
"""

import unittest

from book_log.add_record import parse_command_line, validate_ISBN


class Test_parse_command_line(unittest.TestCase):

    def setUp(self):
        self.test_list = ['test title', 'test author',
                          '0-201-53082-1', 'test genre']

    def test_valid_list_with_no_rating_and_date(self):
        self.assertTupleEqual(parse_command_line(self.test_list),
                              ('test title', 'test author', '0-201-53082-1',
                               'test genre', None, None))

    def test_valid_list_with_rating_but_no_date(self):
        self.test_list.append('4')
        self.assertTupleEqual(parse_command_line(self.test_list),
                              ('test title', 'test author', '0-201-53082-1',
                               'test genre', 4, None))

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

    def test_invalid_list_with_invalid_ISBN(self):
        self.test_list[2] = 'an invalid ISBN'
        self.assertRaisesRegex(ValueError, 'ISBN not in correct format',
                               parse_command_line, self.test_list)


class Test_validate_ISBN(unittest.TestCase):

    def test_10_digit_valid_ISBN_returns_True(self):
        valid_ISBN = '0-201-53082-1'
        self.assertTrue(validate_ISBN(valid_ISBN))

    def test_10_digit_invalid_ISBN_returns_False(self):
        base_ISBN = '0-201-53082-'
        for d in '023456789':
            with self.subTest(d=d):
                self.assertFalse(validate_ISBN(base_ISBN + d))

    def test_13_digit_valid_ISBN_returns_True(self):
        valid_ISBN = '978-0-306-40615-7'
        self.assertTrue(validate_ISBN(valid_ISBN))

    def test_13_digit_invalid_ISBN_returns_False(self):
        base_ISBN = '978-0-306-40615-'
        for d in '012345689':
            with self.subTest(d=d):
                self.assertFalse(validate_ISBN(base_ISBN + d))


if __name__ == '__main__':
    unittest.main()
