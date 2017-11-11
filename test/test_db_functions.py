"""
Test module for db_functions.py
"""

import datetime
import os
import unittest
import sqlite3

from book_log.db_functions import get_connection, create_table, delete_table, \
                                  insert_row, create_record


class Test_get_connection(unittest.TestCase):

    def setUp(self):
        self.conn = get_connection(':memory:')

    def tearDown(self):
        self.conn.close()

    def test_get_connection_is_valid_connection_object(self):
        self.assertIsInstance(self.conn, sqlite3.Connection)


class Test_create_table(unittest.TestCase):

    def setUp(self):
        self.conn = get_connection(':memory:')
        create_table(self.conn, 'books')
        self.table_info = self.conn.execute('PRAGMA table_info(books);')

    def tearDown(self):
        self.conn.close()

    def test_create_table(self):
        self.assertListEqual([r[1] for r in self.table_info.fetchall()],
                             ['Title', 'Author', 'ISBN', 'Genre',
                              'Date_Added', 'Rating'])


class Test_delete_table(unittest.TestCase):

    def setUp(self):
        self.conn = get_connection(':memory:')
        create_table(self.conn, 'books')
        delete_table(self.conn, 'books')
        self.table_info = self.conn.execute('PRAGMA table_info(books);')

    def tearDown(self):
        self.conn.close()

    def test_delete_table(self):
        self.assertListEqual(self.table_info.fetchall(), [])


class Test_insert_row(unittest.TestCase):

    def setUp(self):
        self.conn = get_connection(':memory:')
        create_table(self.conn, 'books')
        self.test_list = ['test title', 'test author',
                          '0-201-53082-1', 'test genre', 'NULL']

    def tearDown(self):
        self.conn.close()

    def test_insert_row_with_no_date_and_no_rating(self):
        insert_row(self.conn, 'books', *self.test_list)
        rows = self.conn.execute('SELECT * FROM books;').fetchall()
        self.test_list = self.test_list[:-1]
        self.test_list.extend([str(datetime.date.today()), None])
        self.assertTupleEqual(rows[0], tuple(self.test_list))

    def test_insert_row_with_rating_but_no_date(self):
        self.test_list[-1] = 4
        insert_row(self.conn, 'books', *self.test_list)
        rows = self.conn.execute('SELECT * FROM books;').fetchall()
        self.test_list.insert(4, str(datetime.date.today()))
        self.assertTupleEqual(rows[0], tuple(self.test_list))

    def test_insert_row_with_date_but_no_rating(self):
        self.test_list.append(datetime.datetime(2005, 12, 10))
        insert_row(self.conn, 'books', *self.test_list)
        rows = self.conn.execute('SELECT * FROM books;').fetchall()
        self.test_list[-2] = '2005-12-10 00:00:00'
        self.test_list[-1] = None
        self.assertTupleEqual(rows[0], tuple(self.test_list))

    def test_insert_row_with_date_and_rating(self):
        self.test_list[-1] = 4
        self.test_list.append(datetime.datetime(2005, 12, 10))
        insert_row(self.conn, 'books', *self.test_list)
        rows = self.conn.execute('SELECT * FROM books;').fetchall()
        self.test_list[-2] = '2005-12-10 00:00:00'
        self.test_list[-1] = 4
        self.assertTupleEqual(rows[0], tuple(self.test_list))


class Test_create_record(unittest.TestCase):

    def setUp(self):
        self.test_filepath = 'test.db'
        self.test_table_name = 'sample'
        os
        self.test_list_1 = ['test title 1', 'test author 1', '0-201-53082-1',
                            'test genre 1', 'NULL',
                            datetime.datetime(2012, 11, 5)]
        self.test_list_2 = ['test title 2', 'test author 2',
                            '978-0-306-40615-7', 'test genre 2', 5]

    def tearDown(self):
        if os.path.exists(self.test_filepath):
            os.remove(self.test_filepath)

    def test_create_record_with_date_but_no_rating(self):
        self.test_list_1.extend([self.test_filepath, self.test_table_name])
        create_record(*self.test_list_1)
        conn = sqlite3.connect(self.test_filepath)
        rows = conn.execute('''SELECT * FROM {test_table_name};
            '''.format(test_table_name=self.test_table_name)).fetchall()
        self.test_list_1 = self.test_list_1[:-2]
        self.test_list_1[-2], self.test_list_1[-1] = '2012-11-05', None
        self.assertTupleEqual(rows[0], tuple(self.test_list_1))

    def test_create_record_with_rating_but_no_date(self):
        self.test_list_2.extend([None, self.test_filepath,
                                 self.test_table_name])
        create_record(*self.test_list_2)
        conn = sqlite3.connect(self.test_filepath)
        rows = conn.execute('''SELECT * FROM {test_table_name};
            '''.format(test_table_name=self.test_table_name)).fetchall()
        self.test_list_2 = self.test_list_2[:-2]
        today = datetime.date.today().__str__()
        self.test_list_2[-2], self.test_list_2[-1] = today, 5
        self.assertTupleEqual(rows[0], tuple(self.test_list_2))


if __name__ == '__main__':
    unittest.main()
