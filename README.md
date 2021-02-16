📦 California housing scraper
============

This repository contains a scraper designed to scrape information from 
https://www.point2homes.com/ in California state.

How to run
======

- Install package to your local machine:
```
pip install git+https://github.com/tiskutis/Capstone24Scraper.git
```
- Run python in your terminal:
```
python
```
- Import scraper and create object:
```
>>> from scraper.Scraper import Scraper
>>> scraper = Scraper()
```
- Call scrape_platform() function and pass how many pages per area you want to scrape (California state has 80
areas in this platform):
```
scraper.scrape_platform(10)
```
Scraped information will be saved to 'California Housing.csv' in your project directory.