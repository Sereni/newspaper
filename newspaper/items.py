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

    text = scrapy.Field()  # clean of everything but <p>. if divs, replace by <p>. insert line breaks between <p>
    author = scrapy.Field()
    date = scrapy.Field()
    source = scrapy.Field()
    wordcount = scrapy.Field()


class Response(scrapy.Item):

    response = scrapy.Field()  # that's the whole response object, yeah, I know
    url = scrapy.Field()

    # ugh, why do we need this response item exactly? can't figure it out
    # it has something to do with the first run.