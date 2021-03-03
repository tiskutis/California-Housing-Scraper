from scraper.Scraper import Scraper
from bs4 import BeautifulSoup as bs, BeautifulSoup

with open("test_data/test_data.html") as f:
    soup = bs(f.read(), "lxml")


def test_page_type():
    scraper = Scraper()
    assert isinstance(soup, BeautifulSoup)


def test_get_price():
    scraper = Scraper()
    assert scraper.get_price(soup) == 998888


def test_get_bedrooms():
    scraper = Scraper()
    assert scraper.get_bedrooms(soup) == 4


def test_get_baths():
    scraper = Scraper()
    assert scraper.get_baths(soup) == 3


def test_get_sqm():
    scraper = Scraper()
    assert scraper.get_sqm(soup) == 232.26


def test_get_lot_size():
    scraper = Scraper()
    assert scraper.get_lot_size(soup) == 0.115


def test_description_dictionary():
    dict_ = {
        "Type": "Residential",
        "Style": "2 Storey",
        "Lot Size": "0.115 Ac",
        "MLS Number": "PW20120310",
        "Year Built": "2012",
        "Parking info": "2, Attached",
        "Zip": "92886",
        "School District": "Placentia-Yorba Linda Unified School District",
    }

    scraper = Scraper()
    assert scraper.description_dictionary(soup) == dict_


def test_demographics_dictionary():
    dict_ = {
        "Total population": "50,545",
        "Male population": "24,484",
        "Female population": "26,061",
        "Median age": "42.80",
        "Total households": "16,559",
        "Average people per household": "3.03",
        "Total housing units": "17,062",
        "Owner occupied": "13,469",
        "Renter occupied": "3,090",
        "Median year built": "1979",
        "Median household income": "123,737",
        "Average household income": "154,190",
    }

    scraper = Scraper()
    assert scraper.demographics_dictionary(soup) == dict_
