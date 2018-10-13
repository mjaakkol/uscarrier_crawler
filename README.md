# uscarrier_crawler

US Mobile operator phone price scraper based on Scrapy+Selenium 

This is web-scraper using [Scrapy](https://scrapy.org/) and [Selenium](https://docs.seleniumhq.org/) to Scrape phone prices from the web-pages of US wireless operators. Currently, only T-Mobile US is supported. The scaper can be invoked using command **_scrapy crawl tmous_**

Scraper outputs the results into JSON-file placed at the the root of the scraper. The filename includes the time-stamp so multiple scrapes can be executed in the same directory. You just want to merge all JSON-files into on eg. Pandas dataframe to start processing them.

---

# How to install

Scraper has been developed using Python 3.6, Scrapy 1.5 and Selenium 3.14.0. It also works with Python 3.7 and likely with the earlier versions as well.

Install Scrapy
Install Selenium
Install [web-driver](https://docs.seleniumhq.org/download/)
Configure the paths properly in settings.py (place the web-driver into path to make your life easier)

Scrape responsibly. Enjoy!

---
# TODO

- Add Verizon
- Add AT&T
