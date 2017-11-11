"""
Module implements database create / read / write functionality
"""

import sqlite3

DB_FILENAME = "sqlite:///book_log/data/book_log.db"
TBL_NAME = "Books"


def get_connection(db_name):
    """Return open database connection"""

    try:
        return sqlite3.connect(db_name)
    except sqlite3.DatabaseError:
        raise


def create_table(conn, tbl_name):
    """Execute SQL statement to add table to database object"""

    CREATE_TABLE_SQL = """CREATE TABLE IF NOT EXISTS {TBL_NAME} (Title TEXT
        NOT NULL, Author TEXT NOT NULL, ISBN TEXT PRIMARY KEY, Genre TEXT NOT
        NULL, Date_Added TEXT NOT NULL DEFAULT CURRENT_DATE, Rating
        INTEGER);""".format(TBL_NAME=tbl_name)

    try:
        conn.execute(CREATE_TABLE_SQL)
    except sqlite3.ProgrammingError:
        raise


def delete_table(conn, tbl_name):
    """Execute SQL statement to delete table from database object"""

    DELETE_TABLE_SQL = 'DROP TABLE IF EXISTS {tbl_name};'.format(**locals())

    try:
        conn.execute(DELETE_TABLE_SQL)
    except sqlite3.ProgrammingError:
        raise


def insert_row(conn, tbl_name, Title, Author, ISBN, Genre,
               Rating='NULL', Date=None):
    """Execute SQL statement to add row into database object"""

    INSERT_RECORD_SQL = '''INSERT INTO {TBL_NAME} (Title, Author, ISBN, Genre,
        Rating'''.format(TBL_NAME=tbl_name)
    INSERT_RECORD_SQL += ', Date)' if Date else ')'
    INSERT_RECORD_SQL += ''' VALUES ("{Title}", "{Author}", "{ISBN}",
        "{Genre}", {Rating}'''.format(**locals())
    INSERT_RECORD_SQL += ', {Date});'.format(**locals()) if Date else ');'

    try:
        conn.execute(INSERT_RECORD_SQL)
    except sqlite3.ProgrammingError:
        raise


def create_record(Title, Author, ISBN, Genre, Rating, Date):
    """Control function for SQL execution"""

    conn = get_connection(DB_FILENAME)

    if conn.execute('PRAGMA table_info(?);', TBL_NAME).fetchall() == []:
        create_table(conn, TBL_NAME)

    insert_row_args = [conn, TBL_NAME, Title, Author, ISBN, Genre]
    if Rating:
        insert_row.append(Rating)
    if Date:
        insert_row_args .append(Date)

    insert_row(*insert_row_args)

    conn.close()
