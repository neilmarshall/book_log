#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 21:31:36 2017

@author: neilmarshall
"""

import argparse

from book_log.db_functions import create_record

__version__ = '1.1.1'


def parse_command_line(*args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('Title')
    parser.add_argument('Author')
    parser.add_argument('ISIN')
    parser.add_argument('Genre')
    parser.add_argument('Rating', type=int, nargs='?')
    args = parser.parse_args(*args)
    # -------------------------------------------------------------------------
    # check that rating, if present, lies within range [1, 5]
    # check that ISIN is in appropriate form (use regexes)
    # -------------------------------------------------------------------------
    return args.Title, args.Author, args.ISIN, args.Genre, args.Rating


def add_record(*args):
    Title, Author, ISIN, Genre, Rating = parse_command_line(*args)
    create_record(Title, Author, ISIN, Genre, Rating)
