# -*- coding: utf-8 -*-
from shutil import which

# Scrapy settings for carrier_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'carrier_crawler'

SPIDER_MODULES = ['carrier_crawler.spiders']
NEWSPIDER_MODULE = 'carrier_crawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'carrier_crawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Various retry and other middleware parameters are disabled as 
# Selenium is doing the requesting part.
RETRY_ENABLED = False
METAREFRESH_ENABLED = False
REDIRECT_ENABLED = False
HTTPERROR_ALLOW_ALL = True
REFERER_ENABLED = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# As this is using Selenium in serialized manner only 2 requests supported

CONCURRENT_REQUESTS = 2


# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'carrier_crawler.middlewares.SeleniumMiddleware' : 400,
#    #'carrier_crawler.middlewares.CarrierCrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'carrier_crawler.middlewares.SeleniumMiddleware' : 800,
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': None
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'carrier_crawler.pipelines.CarrierCrawlerPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# This is using Javascript pages so the content caching doesn't really help.
# Better to disable it.
HTTPCACHE_ENABLED = False

FEED_FORMAT = 'json'
FEED_URI = 'file:%(name)s_dump_%(time)s.json'

LOG_LEVEL = 'INFO'

#Proprietary arguments to control Selenium adaptation
FAILURE_SCREENSHOTS = False
SELENIUM_MIDDLEWARE_RETRYS = 5

# Firefox seems to work the best right now and it is used
# in development. Chrome will likely work as well after some
# of my fixes.
SELENIUM_DRIVER_NAME='Firefox'
SELENIUM_DRIVER_EXECUTABLE_PATH=which('geckodriver.exe')
SELENIUM_DRIVER_ARGUMENTS=['no-sandbox',
                           '--log-level=3']
"""

SELENIUM_DRIVER_NAME='Chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH=which('chromedriver.exe')

SELENIUM_DRIVER_ARGUMENTS=['-headless',   # '--headless' if using chrome instead of firefox
                           'no-sandbox',
                           'disable-gpu',
                           'disable-dev-shm-usage',
#                           'window-size=1200x600',
                           '--log-level=3']
"""

SELENIUM_LOG_LEVEL='WARNING'