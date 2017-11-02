#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 21:31:36 2017

@author: neilmarshall
"""

import argparse

from db_functions import create_record


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('Title')
    parser.add_argument('Author')
    parser.add_argument('ISIN')
    parser.add_argument('Genre')
    parser.add_argument('Rating', type=int, nargs='?')
    args = parser.parse_args()
    # -------------------------------------------------------------------------
    # check that rating, if present, lies within range [1, 5]
    # check that ISIN is in apporpriate form (use regexes)
    # check title / author / genre work if multiple words specified
    # -------------------------------------------------------------------------
    return args.Title, args.Author, args.ISIN, args.Genre, args.Rating


def add_record():
    Title, Author, ISIN, Genre, Rating = parse_command_line()
    print(Title, Author, ISIN, Genre, Rating)
    create_record(Title, Author, ISIN, Genre, Rating)


if __name__ == '__main__':
    add_record()
