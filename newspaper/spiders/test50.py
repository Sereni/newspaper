# coding=utf-8
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
from collections import Counter
from newspaper.items import Response, Article
import newspaper.utils.extract as extract

import os
import re

# todo maybe replace all spiders with one and just provide a start url as an arg


class TestSpider(CrawlSpider):

    # I sort of hope that the args are going to magically appear here, and that this is the way to call them...
    def __init__(self, text=None, author=None, title=None, date=None, first=False, wordcount=10000, *args, **kwargs):

        super(TestSpider, self).__init__()

        # this is supposed to store xpaths
        self.text = text
        self.author = author
        self.title = title
        self.date = date

        # this indicates the first run
        self.first = first

        # set word limit for a download job
        self.limit = wordcount

    names = {
        'kp': 'Комсомольская правда',
        'rbc': 'РБК',
        'sovsport': 'Советский Спорт',  # ооох энкоды полетят
        'ria': 'РИА',
        'izvestia': 'Известия'
    }
    start_urls = []

    def parse_link(self, response):

        if self.first:
            item = Response()
            item['response'] = response
            item['url'] = response.url
        else:
            item = Article()
            item['url'] = response.url
            item['source'] = self.names[self.name]

            # call xpaths one by one and extract data
            # todo add more fields after writing parsers
            if self.text:
                item['text'] = extract.text(response, self.text)

            item['date'] = extract.date(response)
            item['title'] = extract.header(response)

            # you think they'd be empty by default, but no
            item['author'] = ''

        return item

    def update_rules(self, links):

        # substitute all digit sequences with \d+. this is where it breaks if articles have names instead of ids.
        patterns = set([re.sub('\d+', '\d+', link).replace('\\\\', '\\') for link in links])

        # create spider rules based on patterns
        self.rules = tuple([Rule(LinkExtractor(allow=pattern), callback='parse_link', follow=True)
                            for pattern in patterns])

        # update rules
        super(TestSpider, self)._compile_rules()

    def parse_start_url(self, response):

        # get all the nodes that have any text. I did look for better approaches. suggestions welcome.
        nodes = response.xpath('//text()/..')
        previews = []

        # filter text by length, get rid of scripts, write down
        for node in nodes:
            text = node.xpath('./text()').extract()[0]
            if len(text.split()) > 15 and (not 'var' in text and not '{' in text and not '<' in text):
                previews.append(node)

        links = Counter()  # the reason it's a counter is that we'll want to dump anything too frequent later on

        for node in previews:

            # first, check if the node has a href associated with it -- if it does, this is the article link
            self_link = node.xpath('./@href')
            if self_link:
                links[self_link.extract()[0]] += 1
                continue

            # look for previous siblings that are <a> with 2+ words
            # allow to rise for 2 levels of depth to account for divs (if false positives, look here)
            depth = 0
            lift = '../'

            while depth < 3:

                # find the preceding <a> siblings that have text over 2 words long, write down the links
                link_nodes = node.xpath('./{0}preceding-sibling::node()/descendant-or-self::a'.format(lift * depth))
                new_links = [n.xpath('./@href').extract()[0] for n in link_nodes if n.xpath('./text()') and
                             n.xpath('./text()').extract()[0].split() > 2 and
                             n.xpath('./@href')]  # there are a lot of 2-word titles, but also a lot of trash

                # will only go up a level if nothing found on this level. hopefully not that often.
                if new_links:
                    for link in new_links:
                        links[link] += 1
                    break
                depth += 1

        # now process the titles without the preview text
        # collect all links with captions over 5 words long
        nodes = response.xpath('//a')
        for node in nodes:
            if node.xpath('./text()') and len(node.xpath('./text()').extract()[0].split()) > 4:
                url = node.xpath('./@href').extract()[0]
                links[url] += 1

        # filter
        exp = re.compile('\d+')
        link_list = [key for (key, value) in links.items() if value < 3  # repetitive links are usually topics
                     and key.startswith('/')  # relative links only, no externals
                     and exp.search(key)]  # articles often have numbers, sections don't

        self.update_rules(link_list)


class RbcSpider(TestSpider):

    name = 'rbc'
    allowed_domains = ['rbcdaily.ru']
    start_urls = [
        'http://rbcdaily.ru'
    ]


class SovietSpider(TestSpider):
    name = 'sovsport'
    allowed_domains = ['sovsport.ru']
    start_urls = [
        'http://sovsport.ru'
    ]


class RiaSpider(TestSpider):
    name = 'ria'
    allowed_domains = ['ria.ru']
    start_urls = ['http://ria.ru']


class IzvestiaSpider(TestSpider):
    name = 'izvestia'
    allowed_domains = ['izvestia.ru']
    start_urls = ['http://izvestia.ru']

# fixme doesn't find any text or title in kp and records broken xml
# fixme same shit with ria
class KpSpider(TestSpider):
    name = 'kp'
    allowed_domains = ['kp.ru']
    start_urls = ['http://kp.ru']

xpaths = []

# todo add new spider: http://newdaynews.ru/