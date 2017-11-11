"""
Test module for selected actual cases - validates cases work generically
"""

import datetime
import os
import sqlite3
import unittest

from book_log.add_record import parse_command_line
from book_log.db_functions import create_record


class Test_entry_1(unittest.TestCase):

    def setUp(self):
        self.input = ['Chased by Fire', 'D. K. Holmberg', '978-1-522-65783-5',
                      'Fantasy', '2']
        self.output = ['Chased by Fire', 'D. K. Holmberg', '978-1-522-65783-5',
                       'Fantasy', str(datetime.date.today()), 2]
        self.db_filename = 'test.db'
        self.tbl_name = 'test_tbl'

    def tearDown(self):
        if os.path.exists(self.db_filename):
            os.remove(self.db_filename)

    def test_entry_1_with_default_date(self):
        args = parse_command_line(self.input)
        create_record(*args, self.db_filename, self.tbl_name)
        conn = sqlite3.connect(self.db_filename)
        rows = conn.execute('SELECT * FROM {tbl_name};'
                            .format(tbl_name=self.tbl_name)).fetchall()[0]
        self.assertTupleEqual(rows, tuple(self.output))

    def test_entry_1_with_specified_date(self):
        self.input.append('-D 8-11-2017')
        self.output[-2] = str(datetime.date(2017, 11, 8))
        args = parse_command_line(self.input)
        create_record(*args, self.db_filename, self.tbl_name)
        conn = sqlite3.connect(self.db_filename)
        rows = conn.execute('SELECT * FROM {tbl_name};'
                            .format(tbl_name=self.tbl_name)).fetchall()[0]
        self.assertTupleEqual(rows, tuple(self.output))


if __name__ == '__main__':
    unittest.main()
