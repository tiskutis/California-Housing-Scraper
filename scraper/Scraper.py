import requests
from bs4 import BeautifulSoup as bs, BeautifulSoup
import pandas as pd
import numpy as np
import re
import logging


class Scraper:
    """
    This is a scraper class, which can scrape California housing information from https://www.point2homes.com/ website.
    The flow:
    - First, all California areas are extracted and put into a list.
    - Area list is iterated over. Each area has a number of pages with real estate descriptions. User can select how
    many pages he wants to go through.
    - Scraper visits every real estate link in the page and scrapes required information. After all houses are scraped,
    scraper moves to the next page. When no more pages are left or user denoted page limit is reached, scraper
    moves to the next category.
    """

    def __init__(
            self,
            logger=logging.basicConfig(filename='scraping.log', filemode='w', level=logging.DEBUG),
            basic_url: str = 'https://www.point2homes.com'
    ):
        """
        Initialization method
        :param logger: text file to log events
        :param basic_url: url used for to construct new urls.
        """
        self.logger = logger
        self.basic_url = basic_url

    @staticmethod
    def get_page(url_: str) -> BeautifulSoup or None:
        """
        Gets page HTML from the provided url
        :param url_: page you want to scrape from;
        :return: get_page() method queries the provided url and returns response, processed with beautiful soup library;
        if response is not ok, response status_code is printed and None is returned.
        """
        logging.info(f'Getting url: {url_}')

        response = requests.get(url_, headers={"User-Agent": "Mozilla/5.0"})

        if not response.ok:
            logging.error(f'Server response: {response.status_code}')
            return None
        else:
            return bs(response.text, 'lxml')

    @staticmethod
    def get_location_urls(soup: BeautifulSoup) -> list:
        """
        Finds all location links in a page and puts them in a list
        :param soup: BeautifulSoup object
        :return: list with location urls
        """
        location_urls_ = []

        for elem_ in soup.find_all('a', class_='psrk-events'):
            if elem_['href'] not in location_urls_ and "CA" in elem_['href']:
                location_urls_.append(elem_['href'])

        return location_urls_

    @staticmethod
    def get_price(soup: BeautifulSoup) -> float:
        """
        Extracts price from provided BeautifulSoup object
        :param soup: BeautifulSoup object
        :return: price of type int or np.nan if not found
        """
        try:
            price = int(re.findall(r'[0-9][0-9,.]+', soup.find('div', class_="price").
                                   get_text().strip())[0].replace(',', ''))
        except Exception as err:
            logging.warning(f"Price not found. Error message: {err}")
            return np.nan
        return price

    @staticmethod
    def get_bedrooms(soup: BeautifulSoup) -> int or float:
        """
        Extracts number of bedrooms from provided BeautifulSoup object
        :param soup: BeautifulSoup object
        :return: number of bedrooms of type int or np.nan if not found
        """
        try:
            bedrooms = int(re.findall(r'\d+', soup.find("li", class_="ic-beds").get_text().strip())[0])

        except Exception as err:
            logging.warning(f"Bedroom not found. Error message: {err}")
            return np.nan
        return bedrooms

    @staticmethod
    def get_baths(soup: BeautifulSoup) -> int or float:
        """
        Extracts number of baths from provided BeautifulSoup object
        :param soup: BeautifulSoup object
        :return: number of baths of type int or np.nan if not found
        """
        try:
            baths = int(re.findall(r'\d+', soup.find("li", class_="ic-baths").get_text().strip())[0])

        except Exception as err:
            logging.warning(f"Bath not found. Error message: {err}")
            return np.nan
        return baths

    @staticmethod
    def get_sqm(soup: BeautifulSoup) -> float:
        """
        Extracts house size in square meters from provided BeautifulSoup object
        :param soup: BeautifulSoup object
        :return: house size in square meters or np.nan if not found
        """
        try:
            sqm = round(float(re.findall(r'[0-9][0-9,.]+', soup.find("li", class_="ic-sqft")
                                         .get_text().strip())[0].replace(',', '')) / 10.764, 2)
        except Exception as err:
            logging.warning(f"Sqm not found. Error message: {err}")
            return np.nan
        return sqm

    @staticmethod
    def get_lot_size(soup: BeautifulSoup) -> float:
        """
        Extracts lot size in acres from provided BeautifulSoup object
        :param soup: BeautifulSoup object
        :return: lot size in acres or np.nan if not found
        """
        try:
            lot_size = float(
                re.findall(r'[0-9][0-9,.]+', soup.find("li", class_="ic-lotsize").get_text().strip())[0])

        except Exception as err:
            logging.warning(f"Lot size not found. Error message: {err}")
            return np.nan
        return lot_size

    @staticmethod
    def description_dictionary(soup: BeautifulSoup) -> dict:
        """
        Extracts description information, contained in dt and dd elements
        :param soup: BeautifulSoup object
        :return: dictionary with dt as keys and dd as values
        """
        dt_data = soup.find_all("dt")
        dd_data = soup.find_all("dd")

        description = {}

        for dt, dd in zip(dt_data, dd_data):
            description[dt.get_text().strip()] = dd.get_text().strip()

        return description

    @staticmethod
    def demographics_dictionary(soup: BeautifulSoup) -> dict:
        """
        Extracts demographics information, contained in td
        :param soup: BeautifulSoup object
        :return: dictionary with demographics in that area keys (e.g. median income, median age) and values
        """
        demographics = soup.find("div", {"id": "demographics_content"}).find_all('td')
        demographics_ = {}

        for i in range(0, len(demographics), 2):
            demographics_[demographics[i].get_text()] = demographics[i + 1].get_text()

        return demographics_

    def scrape_info_one_house(self, soup: BeautifulSoup) -> dict or None:
        """
        Accepts soup object which contains all the required information about one house.
        Scrapes house type, year built, parking spaces, area population, median age, total households,
        median year built, median household income, number of baths and bedrooms, size in square meters, lot size in
        acres and price.
        :param soup: BeautifulSoup object
        :return: dictionary with all the required info
        """
        house_information = {}

        try:
            description = self.description_dictionary(soup)
            demographics = self.demographics_dictionary(soup)

            house_information['Type'] = description['Type']
            house_information['Year Built'] = description['Year Built']
            house_information['Parking Spaces'] = int(re.findall(r'\d+', description['Parking info'])[0])
            house_information['Area population'] = int(demographics['Total population'].replace(',', ''))
            house_information['Median age'] = demographics['Median age']
            house_information['Total households'] = int(demographics['Total households'].replace(',', ''))
            house_information['Median year built'] = demographics['Median year built']
            house_information['Median household income'] = int(demographics['Median household income'].replace(',', ''))
            house_information['Bedrooms'] = self.get_bedrooms(soup)
            house_information['Baths'] = self.get_baths(soup)
            house_information['Square Meters'] = self.get_sqm(soup)
            house_information['Lot size (acres)'] = self.get_lot_size(soup)
            house_information['Price'] = self.get_price(soup)

            return house_information

        except Exception as err:
            logging.warning(f"Some of the required information was missing for this house. Error message: {err}")
            return None

    def get_houses_in_location(self, location_url_: str,
                               houses_in_location: set = set(),
                               page_limit: int = 1,
                               page_number: int = 1) -> list:
        """
        Accepts location url and goes through pages in that location scraping every house
        until page limit is reached. Returns list of dicts with scraped information about every house in that location.
        :param location_url_: string with link to specific location in California state
        :param houses_in_location: set with already scraped links. Since retrieved links can be repetitive, there is
        no need to go to the same link which has already been scraped. Set is used for faster search
        :param page_limit: how many pages to scraped. If not passed by the user, default is 1
        :param page_number: Current page to scrape. Starting number is 1
        :return: list of dictionaries
        """

        houses_information = []

        try:
            new_url = self.basic_url + location_url_ + f'?page={page_number}'
            page_ = self.get_page(new_url)

            if page_.find_all('li', class_='lslide'):

                for elem in page_.find_all('li', class_='lslide'):
                    link = elem.find('a')['href']
                    if link.startswith('/US') and link not in houses_in_location:
                        houses_information.append(self.scrape_info_one_house(self.get_page(self.basic_url + link)))
                        houses_in_location.add(link)

                if page_number <= page_limit:
                    page_number += 1
                    self.get_houses_in_location(location_url_, houses_in_location, page_limit, page_number=page_number)

        except Exception as err:
            logging.error(f"Error occurred while scraping locations. Message: {err}")

        return houses_information

    def scrape_platform(self, page_limit: int = 1) -> None:
        """
        Main scraping function. Accepts page limit - how many pages to scrape, default is 1.
        The flow:
        - First, all California areas (locations) are extracted and put into a list.
        - Area list is iterated over. Each area has a number of pages with real estate descriptions. User can select how
        many pages he wants to go through.
        - Scraper visits every real estate link in the page and scrapes required information. After all houses are scraped,
        scraper moves to the next page. When no more pages are left or user denoted page limit is reached, scraper
        moves to the next category.
        :param page_limit: how many pages to scrape per area
        :return: None.
        """

        starting_url = 'https://www.point2homes.com/US/Real-Estate-Listings/CA.html'
        houses = []

        starting_page = self.get_page(starting_url)
        locations = self.get_location_urls(starting_page)

        for location in locations:
            houses.extend(self.get_houses_in_location(location, set(), page_limit=page_limit))

        self.to_dataframe(houses).to_csv('California Housing.csv')

    @staticmethod
    def to_dataframe(house_list: list) -> pd.DataFrame:
        """
        Filters out None values and converts the list to pandas DataFrame
        :param house_list: list of dictionaries
        :return: pandas DataFrame
        """
        return pd.DataFrame([house for house in house_list if house is not None])
