# -*- coding: utf-8 -*-
from datetime import date
from re import sub

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, WebDriverException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from ..http import SeleniumRequest

MEM_LOCATION='//*[contains(@class, "memory-btn")]'

RATING_XPATH='//div[@id="BVRRRatingOverall_"]/div[@class="BVRRRatingNormalOutOf"]/span[@class="BVRRNumber BVRRRatingNumber"]'

def selenium_request(request):
    """The current request needs to be turned into SeleniumRequest"""

    # TM symbol is part of href but it is not part of the actual link.
    # Filtering TM symbol seems to do the trick
    url = sub(r'\%ef%bf%bd', '', request.url)

    # Filtering is matching for https://www.t-mobile.com/cell-phone/t-mobile-3-in-1-sim-starter-kit"
    # and https://www.t-mobile.com/cell-phone/t-mobile-linelink-home-phone-adapter either is real phone

    sel_req = SeleniumRequest(url=url,
                              callback=request.callback,
                              meta=request.meta,
                              wait_time=15,
                              wait_until=EC.presence_of_element_located((By.XPATH, MEM_LOCATION))
                            ) if "sim-starter" not in request.url  and "linelink" not in request.url else None

    return sel_req


class TmousSpider(CrawlSpider):
    """Scrapy generated main class for TMO US phone web-site scraping"""
    name = 'tmous'
    allowed_domains = ['t-mobile.com']
    start_url = 'https://www.t-mobile.com/cell-phones'
    items_scraped = 0
    _date = None

    # See Scrapy documentation to see how the contstruct works.
    # Effectively links matching regex for allow are put into scrape-list
    # TODO: deny is probably the best place to to remove sim-starter and linelink
    rules = (
        Rule(
            LinkExtractor(
                allow=(r'\/cell-phone\/[\w-]+'),
                deny=(r'(#|\?)'), #Short 4 '#reviews' & excl.phones w/ '?icid'
                unique=True
            ),
            callback='parse_phone',
            follow=True,
            process_request=selenium_request
        ),
    )

    def start_requests(self):
        self.logger.debug("Start requests ")

        # This works as poor-man's __init__
        self._date = str(date.today())

        try:
            # TMO web-site added funny %e... into href that messes up the actual link
            # those gets filtered off now
            req = SeleniumRequest(url=self.start_url,
                                  wait_time=10,
                                  wait_until=EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "product-grid")]'))
                                  )
        except TimeoutException:
            self.logger.critical("Start request timeout")

        yield req


    def parse_item(self, response):
        """Helper function to go through memory variants"""
        yield self.parse_phone_memory_variant(response, response.meta['memory'])

    def parse_phone_memory_variant(self, response, memory):
        """Main item parsing function"""
        title = response.xpath('//h1[@role="heading"]/text()')\
            .extract_first()\
            .encode('ascii',errors='ignore').decode()

        self.items_scraped += 1
        self.logger.info(f"Processing {title} memory {memory}. {self.items_scraped} items scraped")

        # Static always valid construct
        item = {
            'date': self._date,
            'title' : title,
            'title_unique': f"{title}_{memory}GB",
            'memory' : memory,
        }

        avg_rating = response.xpath(RATING_XPATH + '/text()').extract_first()
        n_ratings = response.xpath('//span[contains(@class, "BVRRCount")]/span[@class="BVRRNumber"]/text()').re_first(r'\d+')

        # Some new products sometimes don't have rating or Javascript gets stuck. Ratings are not vital so
        # they are thrown away in the case they don't come easy. Typically, they are there the next time.
        if avg_rating and n_ratings:
            item['avg_rating'] = float(avg_rating)
            item['n_ratings'] = int(n_ratings)
        else:
            self.logger.warning(f"No rating data available for {title}")

        # This is list of both financed and paying full today prices (financing not always present)
        for p in response.xpath('//div[@class="price-lockup"]'):
            # In all cases there is some kind of upfront payment
            price_down = p.xpath('./span[contains(@class, "cost-price")]/text()').extract_first()

            price_down = float(price_down.replace(',', ''))

            # Just testing if this has montly tag to check if this is finance entry
            if p.xpath('./span[@ng-bind-html="monthlyToday"]'):
                # As monthly is in higher-node, I make the assumptions that it comes first compared
                f_monthly, f_duration = p.xpath('./p[contains(@class, "m-t-10")]//text()').re(r'\d+\.*\d*')

                item.update(
                    {
                        'finance_down': price_down,
                        'finance_monthly': float(f_monthly),
                        'finance_duration': int(f_duration)
                    }
                )
            else:
                item['full_payment'] = price_down

        return item

    def parse_phone(self, response):
        """
        This brings the execution into individual phone page but if there are memory variants
        (like there often is), we need to make another request per page to capture then
        as individual SKUs
        """
        memory_variants = response.xpath(MEM_LOCATION)

        n_variants = len(memory_variants)

        self.logger.info(f"parse phone {response.url} with {n_variants} memory variants")

        # Collecting GB numbers
        in_gbs = ["".join(r.xpath('./text()').extract_first().lower().split()) for r in memory_variants]

        memory = int(sub(r"\D", "", in_gbs[0]))

        self.logger.info(f"parse phone {response.url} with {n_variants} memory variants")

        # Processing the first item as it is already readily available
        yield self.parse_phone_memory_variant(response, memory)

        if n_variants > 1:
            """
            We need to go through all the variants. Nasty but necessary
            from scrapy.shell import inspect_response
            inspect_response(response, self)

            Popping top element off as it is handled by the main path
            """
            in_gbs.pop(0)

            self.logger.info(f"GB list {in_gbs}")

            for gb in in_gbs:
                yield SeleniumRequest(
                    url=f"{response.url}?memory={gb}",
                    callback=self.parse_item,
                    wait_time=20,
                    wait_until=EC.presence_of_element_located((By.XPATH, MEM_LOCATION)),
                    meta = { 'memory' : int(sub(r"\D", "", gb)) }
                    )




