#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict

''' CONSTANTS '''
data = '/Users/samu/Downloads/clippings_export.txt'  # exported from clippings.io
clippings = '/Users/baloghsamuel/python_projects/flask_projects/clippings/data/my_clippings.txt'  # original Kindle clippings format
quotes = OrderedDict()
separator = ' -- '
location = 'loc.'
page = 'pg.'


def build_library():
    ''' Builds clippings library from 'data' and 'clippings' above
    Returns quotes and sorted_quotes (sorted by number of quotes from source) '''
    quotes1 = parse_clippings_io(data)
    quotes2 = parse_my_clippings_txt(clippings)
    quotes = dict(quotes1, **quotes2)
    sorted_by_title_len = OrderedDict(sorted(quotes.items(), key=lambda x: len(x[0]), reverse=True))
    sorted_by_quotes_num = OrderedDict(sorted(quotes.items(), key=lambda x: len(x[1]), reverse=True))
    return quotes, sorted_by_title_len, sorted_by_quotes_num


def parse_clippings_io(data):
    ''' Parses clippings in the format that is the output of www.clippings.io (separator is --) '''
    try:
        with open(data, 'r') as file:
            for line in file.readlines():
                if not line.strip():
                    continue
                else:
                    try:
                        if page in line:
                            quote = line[:line.index(separator)]
                            source = line[line.index(separator) + 4:line.index(page) - 1]
                        elif location in line:
                            quote = line[:line.index(separator)]
                            source = line[line.index(separator) + 4:line.index(location) - 2]
                        else:
                            continue
                        try:
                            quotes[source].append(quote)
                        except KeyError:
                            quotes[source] = [quote]
                    except ValueError:
                        continue
        return quotes
    except (OSError):
        return OrderedDict()

def parse_my_clippings_txt(clippings):
    ''' Parses clippings in the native Kindle format (separator is '("==========") '''
    try:
        with open(clippings, 'r') as file:
            file_as_list = file.read().split("==========")
            for entry in file_as_list:
                if 'Your Highlight' in entry:
                    entry = entry.split('\n')
                    source = entry[1]
                    if source[0] == '\ufeff':
                        source = source[1:]
                    highlight = entry[-2]
                    try:
                        quotes[source].append(highlight)
                    except KeyError:
                        quotes[source] = [highlight]
    except IOError:
        return OrderedDict()
    return quotes
