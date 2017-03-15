""" Search flat results on wg-gesucht.de """
from __future__ import unicode_literals, absolute_import, generators, print_function

from lxml import html
from urllib import urlencode
import requests
from datetime import datetime, timedelta
import locale

locale.setlocale(locale.LC_TIME, str('de_DE.UTF-8'))

class WgGesucht(object):
    """ WG-Gesucht Screen Scraper. """
    def __init__(self):
        """ Initialize with base url """
        self.base_url = 'http://www.wg-gesucht.de/wohnungen-in-Berlin.8.2.0.0.html?'
        self.date = None

    def search(self, category, rent_type, minSize, maxPrice, minRooms, maxRooms, exc=2, balcony=0, pets=0, furnished=0):
        """ Search using a get request including flat details.
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
        params = {'offer_filter': 1, 'city_id': 8,
                  'category': category, 'rent_type': rent_type, 
                  'sMin': minSize, 'rMax': maxPrice,
                 'exc': exc, 'rmMin': minRooms,
                 'rmMax': maxRooms, 'bal': balcony,
                 'pet': pets, 'fur': furnished}
        
        response = requests.get('{}{}'.format(self.base_url, urlencode(params)))
        return self.parse_response(response)

    def grab_xpath_text(self, element, xpath):
        """ Given an element and xpath pattern, return text content.
        :param element: lxml element
        :param xpath: string
        returns string
        """
        data = element.xpath(xpath)
        if len(data) == 1:
            return data[0].text
        elif len(data) > 1:
            return [x.text for x in data]
        return ''

    def parse_response(self, response):
        """ Given a requests response object, return a list of dictionaries
        containing the pertinent flat info.
        :params response: response obj
        returns list of dictionaries
        """
        page = html.fromstring(response.content)
        results = page.xpath('//table/tbody/tr')
        active = [res for res in results if self.grab_xpath_text(
            res, 'td[contains(@class, "datum")]/a/span').replace('\n', '').strip() not in 'inaktiv']
        final_results = []
        for res in active:
            item_dict = {}
            item_dict['rooms'] = self.grab_xpath_text(
                res, 'td[contains(@class, "zimmer")]/a/span').replace('\n', '').strip()
            item_dict['Free from'] = self.grab_xpath_text(
                res, 'td[contains(@class, "freiab")]/a/span').replace('\n', '').strip()
            item_dict['Rent price'] = self.grab_xpath_text(
                res, 'td[contains(@class, "miete")]/a/span/b').replace('\n', '').strip()
            item_dict['Size'] = self.grab_xpath_text(
                res, 'td[contains(@class, "groesse")]/a/span').replace('\n', '').strip()
            item_dict['District'] = self.grab_xpath_text(
                res, 'td[contains(@class, "stadt")]/a/span').replace('\n', '').strip()
            item_dict['Link'] = 'http://www.wg-gesucht.de/'+res.get('adid')
            final_results.append(item_dict)
        return final_results
    
    
