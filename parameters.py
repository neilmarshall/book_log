#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 21:31:36 2017

@author: neilmarshall
"""

DB_FILENAME = "sqlite:///book_log/data/book_log.db"

TBL_NAME = "Books"

CREATE_TABLE_SQL = """CREATE TABLE IF NOT EXISTS {TBL_NAME:s} (Title TEXT
    NOT NULL, Author TEXT NOT NULL, ISBN TEXT PRIMARY KEY, Genre TEXT NOT
    NULL, Date_Added TEXT NOT NULL DEFAULT CURRENT_DATE, Rating
    INTEGER);""".format(**locals())
