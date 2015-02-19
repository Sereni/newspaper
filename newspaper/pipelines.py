# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from collections import Counter
from newspaper.utils.parser import find_text


class NewspaperPipeline(object):
    def process_item(self, item, spider):
        return item


class TextPipeline(object):

    def __init__(self):

        # this stores (text, xpath) found on each page
        self.seen = Counter()
        self.xpaths = Counter()  # now, how do I return the best guess from here when the pipeline closes?

        self.printt = True

    def process_item(self, item, spider):

        # find texts in the response
        texts = find_text(item['response'])

        # remember texts and their xpaths
        self.seen.update(texts)

        while len(texts) > 0:

            # take texts one by one, starting with longest
            best = texts.pop()

            # discard things we've already seen somewhere else
            if self.seen[best] > 3:
                continue

            # if it's good, write to xpaths and quit
            else:
                self.xpaths[best[1]] += 1
                break

        # items go on to the next pipeline
        return item

    # this outputs the pipeline results
    def close_spider(self, spider):

        # todo write it to file or someplace to process later
        print 'article xpath: ', self.xpaths.most_common(1)[0][0]