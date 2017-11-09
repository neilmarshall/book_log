"""
Module defines program-wide parameters used, principallyincluding complex SQL
statements to be executed.
"""

DB_FILENAME = "sqlite:///book_log/data/book_log.db"

TBL_NAME = "Books"

CREATE_TABLE_SQL = """CREATE TABLE IF NOT EXISTS {TBL_NAME} (Title TEXT
    NOT NULL, Author TEXT NOT NULL, ISBN TEXT PRIMARY KEY, Genre TEXT NOT
    NULL, Date_Added TEXT NOT NULL DEFAULT CURRENT_DATE, Rating
    INTEGER);""".format(**locals())
