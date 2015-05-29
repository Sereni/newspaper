# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from collections import Counter
from newspaper.utils.parser import find_text
from scrapy.exceptions import DropItem, CloseSpider
import newspaper.utils.extract as extract
from newspaper.utils.shelari.tokenizator import wordcount
import sys, os
import errno

# ~~~~~ IMPORTANT STUFFS ~~~~~
# whatever xpath you found in a pipeline, output like this:
# sys.stdout.write('fieldname=xpath\n')
# fieldname is the name of field in the Article item (text, author, date, title)
# \n at the end has to be there. please.


class NewspaperPipeline(object):
    def process_item(self, item, spider):
        return item


class WritePipeline(object):

    def __init__(self):

        # store word count
        self.count = 0

    def open_spider(self, spider):
        self.name = spider.name

    def process_item(self, item, spider):
        try:
            # if it is a Response item, pass it along
            item['response']
            return item
        except KeyError:
            # otherwise, it's an article. write to file and don't allow it further

            # create directory. it's a shame I do it every time, but self.name just won't go on __init__
            prefix = os.path.join('downloads')
            self.dir = os.path.join(prefix, self.name)  # breaks here, no?

            if not os.path.exists(self.dir):
                try:
                    os.makedirs(self.dir)
                except OSError as exception:
                    if exception.errno != errno.EEXIST:
                        raise

            # todo create directory based on year and month. include subdir below into path. add existence check
            # subdir = os.path.join(extract.year_month(item['date']))

            path = os.path.join(self.dir, item['url'].strip('/').split('/')[-1])

            # count words in article, save to item['wordcount']
            count = wordcount(item['text'])
            self.count += count
            item['wordcount'] = count

            if self.count > spider.limit:
                raise CloseSpider("Word limit reached")  # this may need to be called inside a spider
                                                         # also, it won't work immediately, I wonder how slow

            with open(path, 'w') as f:
                self.write_item(f, item)
            raise DropItem

    def write_item(self, f, item):

        # I kind of need to use a valid xml constructor
        # but I'm a lazy donkey.
        prefix = '<?xml version="1.0" encoding="utf-8"?>\n<DOCUMENT>\n<METATEXT>\n'
        postfix = '</DOCUMENT>'
        f.write(prefix)
        f.write('<URL>{0}</URL>\n'.format(item['url']))
        f.write('<SOURCE>{0}</SOURCE>\n'.format(item['source']))
        f.write('<DATE>{0}</DATE>\n'.format(item['date']))
        f.write('<AUTHOR>{0}</AUTHOR>\n'.format(item['author']))
        f.write('<TITLE>{0}</TITLE>\n'.format(item['title']))
        f.write('<WORDCOUNT>{0}</WORDCOUNT>\n'.format(item['wordcount']))
        f.write('</METATEXT>\n')
        f.write('<TEXT>{0}</TEXT>'.format(item['text']))
        f.write(postfix)
        f.close()


class TextPipeline(object):

    def __init__(self):

        # this stores (text, xpath) found on each page
        self.seen = Counter()
        self.xpaths = Counter()  # now, how do I return the best guess from here when the pipeline closes?

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
        sys.stdout.write('text=' + str(self.xpaths.most_common(1)[0][0]) + '\n')
