""" Script to compare search across flat sites. """
from __future__ import unicode_literals, absolute_import, generators,     print_function

from wg_gesucht import WgGesucht

import pandas as pd
from datetime import datetime


def prepare_wg_data(results):
    """ Prepare wg-gesucht results in a dataframe so they can be compared. """
    wg_df = pd.DataFrame(results)[2:]
    wg_df['search_engine'] = 'wg-gesucht.de'
    return wg_df


def compare_all(category, rent_type, minSize, maxPrice, minRooms, maxRooms, exc, balcony):
    """ Call search for each of the flat search engines.
    :param category: type of flat
    :param rent_type: type of contract
    :param minSize: minimum size in quare meters
    :param maxPrice: max rent price
    :param minRooms: minimum number of rooms
    :param maxRooms: max number of rooms
    :param exc: exchange flat y/n (optional)
    :param balcony: balcony y/n (optional)
    :param pets: pets allowed (optional)
    :param furnished: furnished y/n (optional)
    """
    wg_api = WgGesucht()
    wg_results = wg_api.search(category, rent_type, minSize, maxPrice, minRooms, maxRooms, exc, balcony)
    final_df = prepare_wg_data(wg_results)
    return final_df


if __name__ == '__main__':
    category = raw_input('what type of flat are you searching for? (enter 0 for WG-Zimmer, 1 for 1-Zimmer-Wohnung, 2 for Wohnung, 3 for Haus) ')
    rent_type = raw_input('where type of contract? (0 for Egal, 1 for limited, 2 for unlimited, 3 for daily rent) ')
    minSize = raw_input('min square meters? ')
    maxPrice = raw_input('max rent in Euro? ')
    minRooms = raw_input('min number of rooms? ')
    maxRooms = raw_input('max number of rooms? ')
    exc = raw_input('exchange flat? (0 for Egal, 1 for Yes, 2 for No)')
    balcony = raw_input('with balcony? (0 for no, 1 for yes)')
    final = compare_all(category, rent_type, minSize, maxPrice, minRooms, maxRooms, exc, balcony)
    print(final)