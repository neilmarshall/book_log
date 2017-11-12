"""
Module implements database create / read / write functionality
"""

import sqlite3

import parameters


def get_connection(db_name):
    """Return open database connection"""

    try:
        return sqlite3.connect(db_name)
    except sqlite3.DatabaseError:
        raise


def create_table(conn, tbl_name):
    """Execute SQL statement to add table to database object"""

    SQL = """CREATE TABLE IF NOT EXISTS {tbl_name} (Title TEXT
        NOT NULL, Author TEXT NOT NULL, ISBN TEXT PRIMARY KEY, Genre TEXT NOT
        NULL, Date_Added TEXT NOT NULL DEFAULT CURRENT_DATE, Rating
        INTEGER);""".format(tbl_name=tbl_name)

    try:
        conn.execute(SQL)
    except sqlite3.ProgrammingError:
        raise


def delete_table(conn, tbl_name):
    """Execute SQL statement to delete table from database object"""

    SQL = 'DROP TABLE IF EXISTS {tbl_name};'.format(**locals())

    try:
        conn.execute(SQL)
    except sqlite3.ProgrammingError:
        raise


def insert_row(conn, tbl_name, Title, Author, ISBN, Genre,
               Rating='NULL', Date=None):
    """Execute SQL statement to add row into database object"""

    SQL = '''INSERT INTO {tbl_name} (Title, Author, ISBN, Genre,
        Rating'''.format(tbl_name=tbl_name)
    SQL += ', Date_Added)' if Date else ')'
    SQL += ''' VALUES ("{Title}", "{Author}", "{ISBN}",
        "{Genre}", {Rating}'''.format(**locals())
    SQL += ', "{Date}");'.format(**locals()) if Date else ');'

    try:
        conn.execute(SQL)
        conn.commit()
    except sqlite3.ProgrammingError:
        raise


def create_record(Title, Author, ISBN, Genre, Rating, Date,
                  db_filename=parameters.DB_FILENAME,
                  tbl_name=parameters.TBL_NAME):
    """
    Control function for SQL execution

    Parameters
    -------
    Title : str
        Title of book

    Author : str
        Author of book

    ISBN : str
        ISBN of book; must be in valid ISBN format

    Genre : str
        Genre of book

    Rating : int
        Book rating; defaults to None, but if provided must lie
        in range [1, 5]

    Date : str
        Date record added; defaults to None, but if provided must be in
        'd-m-yyyy' format

    db_filename : str
        Database file to write to; defaults to variable DB_FILENAME

    tbl_name : str
        Table to write to; defaults to variable TBL_NAME
    """

    conn = get_connection(db_filename)

    # check if table already exists; create it if not
    SQL_TBL_CHECK = 'PRAGMA table_info({tbl_name});'.format(**locals())
    if conn.execute(SQL_TBL_CHECK).fetchall() == []:
        create_table(conn, tbl_name)

    insert_row_args = [conn, tbl_name, Title, Author, ISBN, Genre]
    if Rating:
        insert_row_args.append(Rating)
    if Date:
        insert_row_args.append(Date.strftime('%Y-%m-%d'))

    insert_row(*insert_row_args)

    conn.close()
