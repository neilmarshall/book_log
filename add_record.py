"""
Module defines functions to read in and validate command line arguments,
and create a database record from those arguments.
"""

import argparse
import datetime
import re

from book_log.db_functions import create_record

__version__ = '1.1.1'


def parse_command_line(*args):
    """
    Parse command line arguments

    >>> parse_command_line(['test title', 'test author', '0-201-53082-1', 'test genre'])
    ('test title', 'test author', '0-201-53082-1', 'test genre', None, None)

    >>> parse_command_line(['test title', 'test author', '0-201-53082-1', 'test genre', '1'])
    ('test title', 'test author', '0-201-53082-1', 'test genre', 1, None)

    >>> parse_command_line(['test title', 'test author', '0-201-53082-1', 'test genre', '-D 19-2-2008'])
    ('test title', 'test author', '0-201-53082-1', 'test genre', None, datetime.datetime(2008, 2, 19, 0, 0))

    >>> parse_command_line(['test title', 'test author', '0-201-53082-1', 'test genre', '--Date', '19-2-2008'])
    ('test title', 'test author', '0-201-53082-1', 'test genre', None, datetime.datetime(2008, 2, 19, 0, 0))

    >>> parse_command_line(['test title', 'test author', '0-201-53082-1', 'test genre', '3', '-D 19-2-2008'])
    ('test title', 'test author', '0-201-53082-1', 'test genre', 3, datetime.datetime(2008, 2, 19, 0, 0))

    >>> parse_command_line(['test title', 'test author', '0-201-53082-1', 'test genre', '3', '--Date', '19-2-2008'])
    ('test title', 'test author', '0-201-53082-1', 'test genre', 3, datetime.datetime(2008, 2, 19, 0, 0))
    """

    MIN_RATING, MAX_RATING = 1, 5

    parser = argparse.ArgumentParser(description='''Command line parser
         accepting arguments to instantiate program''')

    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('Title', help='Book title :: string')
    parser.add_argument('Author', help='Book author :: string')
    parser.add_argument('ISBN', help='''Book ISBN :: string - must be in
                        recognised ISBN format''')
    parser.add_argument('Genre', help='Book genre :: string')
    parser.add_argument('Rating', type=int, nargs='?', help='''Book rating ::
                        int - if provided must be between {MIN_RATING} and
                        {MAX_RATING}, else defaults to None
                        '''.format(**locals()))
    parser.add_argument('-D', '--Date',
                        help='Date record added in d-m-yyyy format',
                        type=lambda x: datetime.datetime.strptime(x.strip(),
                                                                  '%d-%m-%Y'))

    args = parser.parse_args(*args)

    if args.Rating is not None:
        ARG_RATING_ERROR_MSG = ('Rating must be between '
                                '{MIN_RATING} and {MAX_RATING}, if present')
        if args.Rating not in range(MIN_RATING, MAX_RATING + 1):
            raise ValueError(ARG_RATING_ERROR_MSG.format(**locals()))

    if not validate_ISBN(args.ISBN):
        raise ValueError('ISBN not in correct format')

    return args.Title, args.Author, args.ISBN, args.Genre, args.Rating, \
        args.Date


def validate_ISBN(ISBN):
    """
    Validate if a given ISBN in correct format
    """

    pat = r'((978|979)(-))?(\d)-(\d{3})-(\d{5})-(\d)'
    is_valid_ISBN = re.match(pat, ISBN) is not None

    ISBN_digits = ''.join([d for d in ISBN if d in '0123456789'])

    if len(ISBN_digits) == 10:
        weights = list(range(10, 0, -1))
        checksum = sum(map(lambda x: x[0] * x[1],
                           zip(map(int, ISBN_digits), weights)))
        if checksum % 11 != 0:
            is_valid_ISBN = False
    elif len(ISBN_digits) == 13:
        weights = [1, 3] * 6
        checksum = sum(map(lambda x: x[0] * x[1],
                           zip(map(int, ISBN_digits[:-1]), weights))) % 10
        if not (checksum == 0 or 10 - checksum == int(ISBN_digits[-1])):
            is_valid_ISBN = False

    return is_valid_ISBN


def add_record(*args):
    """
    Read in and validate command line arguments and create database record

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

    Rating : str
        String representation of rating; optional, but if provided must lie
        in range [1, 5]

    Date : str
        Date record added; optional, but if provided must be in 'd-m-yyyy'
        format
    """

    Title, Author, ISBN, Genre, Rating, Date = parse_command_line(*args)

    create_record(Title, Author, ISBN, Genre, Rating, Date)
