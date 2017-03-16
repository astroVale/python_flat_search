""" Script to compare search across flat sites. """
from __future__ import unicode_literals, absolute_import, generators,     print_function

from wg_gesucht import WgGesucht

import pandas as pd


def prepare_wg_data(results):
    """ Prepare wg-gesucht results in a dataframe so they can be compared. """
    wg_df = pd.DataFrame(results)
    wg_df['search_engine'] = 'wg-gesucht.de'
    return wg_df


def compare_all(category, rent_type, minSize, maxPrice, minRooms, maxRooms, exc, balcony, pets, furnished):
    """ Call search for each of the flat search engines.
    :param category: type of flat, limited to Wohnung for now
    :param rent_type: type of contract
    :param minSize: minimum size in square meters
    :param maxPrice: max rent price
    :param minRooms: minimum number of rooms
    :param maxRooms: max number of rooms
    :param exc: exchange flat y/n (optional)
    :param balcony: balcony y/n (optional)
    :param pets: pets allowed (optional)
    :param furnished: furnished y/n (optional)
    """
    wg_api = WgGesucht()
    wg_results = wg_api.search(category, rent_type, minSize, maxPrice, minRooms, maxRooms, exc, balcony, pets, furnished)
    final_df = prepare_wg_data(wg_results)
    final_df.to_csv('Flat_search_results.csv', sep=str('\t'), encoding='utf-8')  # saving into csv file
    return final_df


if __name__ == '__main__':
    category = raw_input('what type of flat are you searching for? (enter 2 for Wohnung) ') or '2'
    rent_type = raw_input(
        'where type of contract? (0 for Egal, 1 for limited, 2 for unlimited, 3 for daily rent) ') or '0'
    minSize = raw_input('min square meters? ')
    maxPrice = raw_input('max rent in Euro? ')
    minRooms = raw_input('min number of rooms? Optional(>=2)') or '2'
    maxRooms = raw_input('max number of rooms? Optional') or '0'
    exc = raw_input('swap flat? Optional (Press Enter for Egal, 1 for Yes, 2 for No)') or '2'
    balcony = raw_input('with balcony? Optional(0 for no, 1 for yes)') or '0'
    pets = raw_input('pets allowed? Optional(Press Enter for Egal, 1 for Yes)') or '0'
    furnished = raw_input('furnished? Optional(Press Enter for Egal, 1 for Yes, 2 for No)') or '0'
    final = compare_all(category, rent_type, minSize, maxPrice, minRooms, maxRooms, exc, balcony, pets, furnished)
    print(final)