# -*- coding: utf-8 -*-

# Scrapy settings for newspaper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'newspaper'

SPIDER_MODULES = ['newspaper.spiders']
NEWSPIDER_MODULE = 'newspaper.spiders'

LOG_LEVEL = 'INFO'
COOKIES_ENABLED = False

# this will result in approx 50 pages, since crawls are async and do not stop immediately
# CLOSESPIDER_PAGECOUNT = 42

# this setting is for quick tests
CLOSESPIDER_PAGECOUNT = 2

# this helps against 503s on some sites
DOWNLOAD_DELAY = 1

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'newspaper (+http://www.yourdomain.com)'
