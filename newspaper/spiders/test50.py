__author__ = 'Sereni'
"""
This module downloads a sample html corpus.
Run
$ scrapy crawl %spidername%
in the project folder, where %spidername% comes
from the name variable in each class.
"""

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

import os
import errno


class TestSpider(CrawlSpider):

    dir = ''
    prefix = 'newspaper/downloads/'

    def parse_link(self, response):

        self.dir = self.prefix + self.name
        path = self.dir + '/' + response.url.strip('/').split('/')[-1]

        if not os.path.exists(self.dir):
            try:
                os.makedirs(self.dir)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise

        with open(path, 'w') as f:
            f.write(response.body)


class RbcSpider(TestSpider):

    name = 'rbc'
    allowed_domains = ['rbcdaily.ru']
    start_urls = [
        'http://rbcdaily.ru'
    ]

    rules = (
        Rule(LinkExtractor(allow='/[\w]+/[0-9]+'), callback='parse_link', follow=True),
    )


class SovietSpider(TestSpider):
    name = 'sovsport'
    allowed_domains = ['sovsport.ru']
    start_urls = [
        'http://sovsport.ru'
    ]

    rules = (
        Rule(LinkExtractor(allow='/[\w]+/(text|article)-item/[0-9]+'), callback='parse_link', follow=True),
    )


class RiaSpider(TestSpider):
    name = 'ria'
    allowed_domains = ['ria.ru']
    start_urls = ['http://ria.ru']

    rules = (
        Rule(LinkExtractor(allow='/[\w]+/[0-9]+/[0-9]+.html'), callback='parse_link', follow=True),
    )


class IzvestiaSpider(TestSpider):
    name = 'izvestia'
    allowed_domains = ['izvestia.ru']
    start_urls = ['http://izvestia.ru']

    rules = (
        Rule(LinkExtractor(allow='/news/[0-9]+'), callback='parse_link', follow=True),
    )


class KpSpider(TestSpider):
    name = 'kp'
    allowed_domains = ['kp.ru']
    start_urls = ['http://kp.ru']

    rules = (
        Rule(LinkExtractor(allow='/online/news/[0-9]+'), callback='parse_link', follow=True),
    )