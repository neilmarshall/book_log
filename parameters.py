DB_FILENAME = "book_log/data/book_log.db"

TBL_NAME = "Books"

TBL_SCHEMA = ['Title TEXT NOT NULL', 'Author TEXT NOT NULL',
              'ISBN TEXT PRIMARY KEY', 'Genre TEXT NOT NULL',
              'Date_Added TEXT NOT NULL DEFAULT CURRENT_DATE',
              'Rating INTEGER']
