# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Article(scrapy.Item):

    # for the tutorial, we'll only be collecting titles
    title = scrapy.Field()
    url = scrapy.Field()

    # text = scrapy.Field()
    # author = scrapy.Field()
    # date = scrapy.Field()


class Response(scrapy.Item):

    response = scrapy.Field()  # that's the whole response object, yeah, I know
    url = scrapy.Field()