"""
Module implements database create / read / write functionality
"""

import sqlite3

from book_log.parameters import DB_FILENAME, TBL_NAME, CREATE_TABLE_SQL


def get_connection(db_name):
    """Return open database connection"""

    try:
        conn = sqlite3.connect(db_name)
        return conn
    except sqlite3.DatabaseError:
        raise sqlite3.DatabaseError('ERROR: COULD NOT OPEN DATABASE')


def create_table(conn):
    """Execute SQL statement to add table to database object"""

    try:
        conn.execute(CREATE_TABLE_SQL)
    except sqlite3.ProgrammingError:
        raise sqlite3.ProgrammingError(CREATE_TABLE_SQL)


def delete_table(conn, tbl_name):
    """Execute SQL statement to delete table from database object"""

    DELETE_TABLE_SQL = 'DROP TABLE IF EXISTS {tbl_name};'.format(**locals())

    try:
        conn.execute(DELETE_TABLE_SQL)
    except sqlite3.ProgrammingError:
        raise sqlite3.ProgrammingError(DELETE_TABLE_SQL)


def insert_row(conn, Title, Author, ISBN, Genre, Rating):
    """Execute SQL statement to add row into database object"""

    INSERT_RECORD_SQL = '''INSERT INTO {TBL_NAME} (Title, Author, ISBN, Genre,
        Rating) VALUES ("{Title}", "{Author}", "{ISBN}", "{Genre}", {Rating});
        '''.format(TBL_NAME=TBL_NAME, **locals())

    try:
        conn.execute(INSERT_RECORD_SQL)
    except sqlite3.ProgrammingError:
        raise sqlite3.ProgrammingError(INSERT_RECORD_SQL)


def create_record(Title, Author, ISBN, Genre, Rating=None):
    """Control function for SQL execution"""

    conn = get_connection(DB_FILENAME)

    if conn.exeecute('PRAGMA table_info(invalid_table);').fetchall() == []:
        create_table(conn)

    insert_row(conn, Title, Author, ISBN, Genre,
               "NULL" if Rating is None else Rating)

    conn.close()
