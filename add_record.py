"""
Module defines functions to read in and validate command line arguments,
and create a database record from those arguments.
"""

import argparse
import re

from book_log.db_functions import create_record

__version__ = '1.1.1'


def parse_command_line(*args):
    """
    Parse command line arguments
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('Title')
    parser.add_argument('Author')
    parser.add_argument('ISBN')
    parser.add_argument('Genre')
    parser.add_argument('Rating', type=int, nargs='?')

    args = parser.parse_args(*args)

    if args.Rating is not None:
        if args.Rating not in [1, 2, 3, 4, 5]:
            raise ValueError('Rating must be between 1 and 5, if supplied')

    if not validate_ISBN(args.ISBN):
        raise ValueError('ISBN not in correct format')

    return args.Title, args.Author, args.ISBN, args.Genre, args.Rating


def validate_ISBN(ISBN):
    """
    Validate if a given ISBN in correct format
    """

    ISBN_digits = ''.join([d for d in ISBN if d in '0123456789'])

    pat = r'(978|979)?([\d]{2})([\d]{4})([\d]{3})(\d)'

    is_valid_ISBN = re.match(pat, ISBN_digits) is not None

    if len(ISBN_digits) == 10:
        weights = list(range(10, 0, -1))
        checksum = sum(map(lambda x: x[0] * x[1],
                           zip(map(int, ISBN_digits), weights)))
    elif len(ISBN_digits) == 13:
        weights = [1, 3] * 6
        checksum = sum(map(lambda x: x[0] * x[1],
                           zip(map(int, ISBN_digits[:-1]), weights)))
    else:
        weights = None
        checksum = None

    if checksum is not None:
        if len(ISBN_digits) == 10:
            if checksum % 11 != 0:
                is_valid_ISBN = False
        elif len(ISBN_digits) == 13:
            checksum = checksum % 10
            if not (checksum == 0 or 10 - checksum == int(ISBN_digits[-1])):
                is_valid_ISBN = False
        else:
            raise RuntimeError
    else:
        is_valid_ISBN = False

    return is_valid_ISBN


def add_record(*args):
    """
    Read in and validate command line arguments and create database record
    """

    Title, Author, ISBN, Genre, Rating = parse_command_line(*args)

    create_record(Title, Author, ISBN, Genre, Rating)
