""" Search flat results on wg-gesucht.de """
from __future__ import unicode_literals, absolute_import, generators, print_function

from lxml import html
from urllib import urlencode
import requests
import time
import random
import locale

locale.setlocale(locale.LC_TIME, str('de_DE.UTF-8'))

class WgGesucht(object):
    """ WG-Gesucht Screen Scraper. """
    def __init__(self):
        """ Initialize with base url """
        self.base_url = 'http://www.wg-gesucht.de/wohnungen-in-Berlin.8.2.0.{}.html?'

    def search(self, category, rent_type, minSize, maxPrice, minRooms, maxRooms, exc, balcony, pets, furnished):
        """ Search using a get request including flat details.
        :param category: type of flat
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
        params = {'offer_filter': 1, 'city_id': 8,
                  'category': category, 'rent_type': rent_type, 
                  'sMin': minSize, 'rMax': maxPrice,
                  'rmMin': minRooms, 'rmMax': maxRooms,
                  'exc': exc, 'bal': balcony,
                 'pet': pets, 'fur': furnished}

        session = requests.Session()
        response = session.get('{}{}'.format(self.base_url.format('0'), urlencode(params)))
        print(response.url)
        results = self.parse_response(response)[0]

        max_page = self.has_more_pages(response)
        if max_page:
            stop = False
            for i in range(1, max_page):
                time.sleep(random.randint(1, 3))
                if stop:
                    break
                r = session.get(self.base_url.format(i))
                print(r.url)
                next_pages, stop = self.parse_response(r)
                results.extend(next_pages)
        return results

    def has_more_pages(self, response):
        page = html.fromstring(response.content)
        try:
            max_page = int(page.xpath('//a[@class="a-pagination"][last()]')[-1].text.replace('\n', '').strip())
        except Exception as IndexError:
            print('Only one page results')
            max_page = False
        return max_page

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
        stop = False
        page = html.fromstring(response.content)
        results = page.xpath('//table/tbody/tr')
        active_inactive = [self.grab_xpath_text
                           (res, 'td[contains(@class, "datum")]/a/span').replace('\n', '').strip() not in 'inaktiv' for res in results]
        final_results = []
        for is_active, res in zip(active_inactive[2:], results[2:]):
            if not is_active:
                stop = True
                break
            item_dict = {}
            item_dict['rooms'] = self.grab_xpath_text(
                res, 'td[contains(@class, "zimmer")]/a/span').replace('\n', '').strip()
            if not item_dict['rooms']:
                item_dict['rooms'] = '1'
            item_dict['Free from'] = self.grab_xpath_text(
                res, 'td[contains(@class, "freiab")]/a/span').replace('\n', '').strip()
            item_dict['Free until'] = self.grab_xpath_text(
                res, 'td[contains(@class, "freibis")]/a/span').replace('\n', '').strip()
            item_dict['Rent price'] = self.grab_xpath_text(
                res, 'td[contains(@class, "miete")]/a/span/b').replace('\n', '').strip()
            item_dict['Size'] = self.grab_xpath_text(
                res, 'td[contains(@class, "groesse")]/a/span').replace('\n', '').strip()
            item_dict['District'] = self.grab_xpath_text(
                res, 'td[contains(@class, "stadt")]/a/span').replace('\n', '').strip()
            item_dict['Link'] = 'http://www.wg-gesucht.de/'+res.get('adid')
            final_results.append(item_dict)
        return final_results, stop
    
    
