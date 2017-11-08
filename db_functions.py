#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 21:31:36 2017

@author: neilmarshall
"""

import sqlalchemy

from book_log.parameters import DB_FILENAME, TBL_NAME, CREATE_TABLE_SQL


def get_connection(db_name):
    try:
        engine = sqlalchemy.create_engine(db_name)
        conn = engine.connect()
        return conn
    except sqlalchemy.exc.SQLAlchemyError:
        raise sqlalchemy.exc.SQLAlchemyError('ERROR: COULD NOT OPEN DATABASE')


def create_table(db_name):
    conn = get_connection(db_name)
    try:
        conn.execute(CREATE_TABLE_SQL)
    except sqlalchemy.exc.StatementError:
        raise sqlalchemy.exc.StatementError(CREATE_TABLE_SQL)
    finally:
        conn.close()


def delete_table(db_name, tbl_name):
    conn = get_connection(db_name)
    DELETE_TABLE_SQL = 'DROP TABLE IF EXISTS {tbl_name};'.format(**locals())
    if not conn.engine.has_table(tbl_name):
        raise sqlalchemy.exc.NoSuchTableError(
                '{tbl_name} not found'.format(**locals()))
    try:
        conn.execute()
    except sqlalchemy.exc.StatementError:
        raise sqlalchemy.exc.StatementError('''Error with following SQL
            statement: "{DELETE_TABLE_SQL}";'''.format(**locals()))
    finally:
        conn.close()


def create_record(Title, Author, ISBN, Genre, Rating=None):
    conn = get_connection(DB_FILENAME)
    if Rating is None:
        Rating = "NULL"
    if not conn.engine.has_table(TBL_NAME):
        create_table(DB_FILENAME)
    INSERT_RECORD_SQL = '''INSERT INTO {TBL_NAME} (Title, Author, ISBN, Genre,
        Rating) VALUES ("{Title}", "{Author}", "{ISBN}", "{Genre}", {Rating});
        '''.format(TBL_NAME=TBL_NAME, **locals())

    try:
        conn.execute(INSERT_RECORD_SQL)
    except sqlalchemy.exc.StatementError:
        raise sqlalchemy.exc.StatementError(INSERT_RECORD_SQL)
    finally:
        conn.close()
