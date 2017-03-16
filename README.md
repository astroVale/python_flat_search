# python_flat_search
Webscraping project with Python for flat searching in Berlin.

Based on the [Python Flight Search](https://github.com/kjam/python_flight_search) project by kjam.  

## Scripts:
* wg-gesucht_scraped.ipynb - Jupyther Notebook script to scrape [wg-gesucht.de](http://wg-gesucht.de) website. It run a search for flats according to input parameters and returns results in a `pandas` DataFrame.
* wg_gesucht.py - Python script to scrape flats for rent in [wg-gesucht.de](http://wg-gesucht.de).
* main.py - Main script to run and get csv file of the search results.

All script are written in Python 2 so some modification may be needed in case using Python 3.

## To Do:
* Extend script for searching also 1-room flats and room in shared flats.
* Extend to a series of Python scripts for scraping other websites.
* Search on all websites and compare the results in `pandas` DataFrame / csv.
