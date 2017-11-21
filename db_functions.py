"""
Module implements database create / read / write functionality
"""

import sqlite3

import book_log.parameters as parameters


def get_connection(db_name):
    """Return open database connection"""

    try:
        return sqlite3.connect(db_name)
    except sqlite3.DatabaseError:
        raise sqlite3.DatabaseError('Could not connect to database')


def create_table(conn, tbl_name, tbl_schema):
    """Execute SQL statement to add table to database object"""

    # construct SQL 'CREATE TABLE' query from schema in 'parameters' module
    SQL = "CREATE TABLE IF NOT EXISTS {tbl_name} (".format(tbl_name=tbl_name)
    SQL += (', ').join(tbl_schema)
    SQL += ");"

    try:
        conn.execute(SQL)
    except sqlite3.ProgrammingError:
        raise sqlite3.DatabaseError(SQL)


def delete_table(conn, tbl_name):
    """Execute SQL statement to delete table from database object"""

    SQL = 'DROP TABLE IF EXISTS {tbl_name};'.format(**locals())

    try:
        conn.execute(SQL)
    except sqlite3.ProgrammingError:
        raise sqlite3.DatabaseError(SQL)


def insert_row(conn, tbl_name, Title, Author, ISBN, Genre,
               Rating='NULL', Date=None):
    """Execute SQL statement to add row into database object"""

    SQL = '''INSERT INTO {tbl_name} (Title, Author, ISBN, Genre,
        Rating'''.format(**locals())
    SQL += ', Date_Added)' if Date else ')'
    SQL += ''' VALUES ("{Title}", "{Author}", "{ISBN}",
        "{Genre}", {Rating}'''.format(**locals())
    SQL += ', "{Date}");'.format(**locals()) if Date else ');'

    try:
        conn.execute(SQL)
        conn.commit()
    except sqlite3.ProgrammingError:
        raise sqlite3.DatabaseError(SQL)


def create_record(Title, Author, ISBN, Genre, Rating, Date,
                  db_filename=parameters.DB_FILENAME,
                  tbl_name=parameters.TBL_NAME,
                  tbl_schema=parameters.TBL_SCHEMA):
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
        create_table(conn, tbl_name, tbl_schema)

    positional_args = [conn, tbl_name, Title, Author, ISBN, Genre]
    optional_args = {}
    if Rating:
        optional_args['Rating'] = Rating
    if Date:
        optional_args['Date'] = Date.strftime('%Y-%m-%d')

    insert_row(*positional_args, **optional_args)

    conn.close()
