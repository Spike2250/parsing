#!/usr/bin/env python3
from parse.two_gis.main import parse
from search_settings import SEARCH_QUERY, CITY


def main():
    parse(SEARCH_QUERY) if CITY == '' else parse(SEARCH_QUERY, CITY)


if __name__ == '__main__':
    main()
