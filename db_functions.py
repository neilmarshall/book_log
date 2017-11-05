#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 21:31:36 2017

@author: neilmarshall
"""

import sqlalchemy

from parameters import DB_FILENAME, TBL_NAME, CREATE_TABLE_SQL, \
                       DELETE_TABLE_SQL


def get_connection():
    try:
        engine = sqlalchemy.create_engine(DB_FILENAME)
        conn = engine.connect()
    except sqlalchemy.exc.SQLAlchemyError:
        raise
    return conn


def create_table():
    conn = get_connection()
    if conn is not None:
        try:
            conn.execute(CREATE_TABLE_SQL)
        except sqlalchemy.exc.StatementError:
            raise
        finally:
            conn.close()
    else:
        raise RuntimeError('database connection failed')


def delete_table():
    conn = get_connection()
    if conn is not None:
        try:
            conn.execute(DELETE_TABLE_SQL)
        except sqlalchemy.exc.StatementError:
            raise
        finally:
            conn.close()
    else:
        raise RuntimeError('database connection failed')


def create_record(Title, Author, ISIN, Genre, Rating=None):
    if Rating is None:
        Rating = "NULL"
    params = locals()
    params.update({'TBL_NAME': TBL_NAME})
    conn = get_connection()
    if conn is not None:
        if not conn.engine.has_table(TBL_NAME):
            create_table()
        try:
            conn.execute('''INSERT INTO {TBL_NAME} (Title, Author, ISIN,
                         Genre, Rating) VALUES ("{Title}", "{Author}",
                         "{ISIN}", "{Genre}", {Rating});'''.format(**params))
        except sqlalchemy.exc.StatementError:
            raise
        finally:
            conn.close()
    else:
        raise RuntimeError('database connection failed')
