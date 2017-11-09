#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 22:40:16 2017

@author: neilmarshall
"""

import unittest

import sqlalchemy

from book_log.db_functions import get_connection, create_table, \
                                  delete_table, create_record


class Test_get_connection(unittest.TestCase):
    
    def setUp(self):
        conn = get_connection('sqlite://')
    
    def tearDown(self):
        conn.close()

    def test_get_connection(self):
        self.assertIsInstance(conn, sqlalchemy.engine.Connection)


class Test_create_table(unittest.TestCase):

    def setUp(self):
        conn = get_connection('sqlite://')
    
    def tearDown(self):
        conn.close()

    @unittest.skip("'Test_create_table' class not yet implemented")
    def test_create_table(self):
        pass


class Test_delete_table(unittest.TestCase):

    def setUp(self):
        conn = get_connection('sqlite://')
    
    def tearDown(self):
        conn.close()

    @unittest.skip("'Test_delete_table' class not yet implemented")
    def test_delete_table(self):
        pass


class Test_create_record(unittest.TestCase):

    def setUp(self):
        conn = get_connection('sqlite://')
    
    def tearDown(self):
        conn.close()

    @unittest.skip("'Test_create_record' class not yet implemented")
    def test_create_record(self):
        pass
