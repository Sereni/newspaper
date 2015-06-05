# coding=utf-8

import re
from lxml import etree
import os
import codecs


def text(response, xpath):
    """
    Given a response and an xpath, get text inside xpath separated with <p> tags
    """
    article_text = u''

    # get everything inside xpath tag
    nodes = response.xpath(xpath)

    for node in nodes:

        # get node tag to filter randomness. hm, this might break
        name = node.xpath('name(.)').extract()[0]
        if name == 'div':

            # get text of node and its descendants, write between <p>s and append to text
            text = re.sub('(\n)+', '</p>\n<p>', ' '.join(node.xpath("string(.)").extract()))
            article_text = article_text + u'<p>{0}</p>\r\n'.format(text)

        # fixme that stuff's broken
        # I think what it actually does, is it takes the upper-level tag, and replaces all \n's in it
        # what you need is to take the text with html tags inside the upper-level tag, replace all divs with p's,
        # and then strip everything but p's

        # if the tags are p, sovsport inserts \n at every line break, and we end up with tons of fake <p>'s.
        # so don't replace line breaks in this case
        elif name == 'p':
            article_text = article_text + u'{0}\r\n'.format(' '.join(node.xpath("string(.)").extract()))


    return article_text


def year_month(s):
    """
    Given item's date in some fixed format, return year and month to use in folder names
    """
    day, month, year = s.split('.')
    return year, month

# input: path to file, output: date
# use in the main pipeline at each file

# to convert date to the format d(d).mm.yy(yy)
def convert_date(raw_date):
    # for replacing the words by numbers at the end
    months = {u'января': u'01', u'февраля': u'02', u'марта': u'03', u'апреля': u'04',
              u'мая': u'05', u'июня': u'06', u'июля': u'07', u'августа': u'08',
              u'сентября': u'09', u'октября': u'10', u'ноября': u'11', u'декабря': u'12',
              u'Января': u'01', u'Февраля': u'02', u'Марта': u'03', u'Апреля': u'04',
              u'Мая': u'05', u'Июня': u'06', u'Июля': u'07', u'Августа': u'08',
              u'Сентября': u'09', u'Октября': u'10', u'Ноября': u'11', u'Декабря': u'12'}

    # transform month from word to mm. format
    for month in months:
        if month in raw_date:
            raw_date = raw_date.replace(month, months[month])
            found_date = re.search(u'([0-9]{1,2}[.-/ ][0-9]{1,2}[.-/ ][0-9]{2,4}).*', raw_date)  # to delete time
            if found_date is not None:
                raw_date = found_date.group(1)

    result_date = re.sub(u'[ /-]', u'.', raw_date)
    return result_date

# article is a path to an *.html file
# MODIFIED by K: article is a html response from scrapy
def date(article):
    # main regex
    search_date = re.compile(u'([0-9]{1,2}[.-/ ]'
                             u'([0-9]{2}'
                             u'|[Яя]нваря|[Фф]евраля|[Мм]арта|[Аа]преля|[Мм]ая|[Ии]юня|'
                             u'[Ии]юля|[Аа]вгуста|[Сс]ентября|[Оо]ктября|[Нн]оября|[Дд]екабря)'
                             u'[.-/ ]20[0-9]{2,4}).*')
    # f = codecs.open(article, 'r', 'utf-8')
    # text = f.read()

    text = article.body  # article is a Scrapy Response object

    # content -- every text in div
    content = []
    root = etree.XML(text, etree.HTMLParser())
    # raw date can contain months as words; result date -- only numbers
    raw_date = ''

    # check date in URl -- must be the first check
    # ...

    for d in root.iter():

        # easy cases: date/time tags, attributes, values of attributes

        # case for sovsport with 'time'
        if d.tag == 'time' or d.tag == 'date':
            if d.text is not None:
                d.text = ' '.join(d.text.split())
                found_date = re.search(search_date, d.text)
                if found_date is not None:
                    raw_date = found_date.group(1)
                    result_date = convert_date(raw_date)
                    return result_date

        # case for izvestia with 'date'
        if 'time' in d.attrib or 'date' in d.attrib:
            d.attrib = ' '.join(d.attrib.split())
            found_date = re.search(search_date, d.attrib)
            if found_date is not None:
                raw_date = found_date.group(1)
                result_date = convert_date(raw_date)
                return result_date

        # case for rbc with 'date'
        for attr in d.attrib:
            if 'time' in d.attrib[attr] or 'date' in d.attrib[attr]:
                if d.text is not None:
                    d.text = ' '.join(d.text.split())
                    found_date = re.search(search_date, d.text)
                    if found_date is not None:
                        raw_date = found_date.group(1)
                        result_date = convert_date(raw_date)
                        return result_date

        # if nothing is found by now -- collect text from divs
        if d.tag == 'div' or d.tag == 'span':
            for child in d:
                if child.tag != 'script': # prevent collecting js scripts
                    if child.text is not None:
                        child.text = child.text.strip(' \t\n\r') # some dates are written in several lines with tabs
                        if child.text != '':
                            content.append(child.text)

    # searching in content for the possible dates
    possible_dates = []
    if raw_date == '':
        for i in range(len(content)):
            found_date = re.search(search_date, content[i])
            if found_date is not None:
                # case for ria
                # idea: likes from social networks are close to date
                # maybe make it more sophisticated -- nearby content, not only i-1
                if u'Нравится' in content[i-1]:
                    raw_date = found_date.group(1)
                    result_date = convert_date(raw_date)
                    return result_date
                possible_dates.append(found_date.group(1))

        # going through all possible dates
        if len(possible_dates) == 1:
            raw_date = possible_dates[0]
            result_date = convert_date(raw_date)
            return result_date
        elif len(possible_dates) > 1:
            for i in range(len(possible_dates)-1):
                # case for kp
                # if date appears several times; one after another
                if possible_dates[i] == possible_dates[i+1]:
                    raw_date = possible_dates[i]
    result_date = convert_date(raw_date)
    return result_date


def lcs(a, b):
    lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
    # row 0 and column 0 are initialized to 0 already
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i+1][j+1] = lengths[i][j] + 1
            else:
                lengths[i+1][j+1] = \
                    max(lengths[i+1][j], lengths[i][j+1])
    # read the substring out from the matrix
    result = ""
    x, y = len(a), len(b)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x-1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y-1]:
            y -= 1
        else:
            assert a[x-1] == b[y-1]
            result = a[x-1] + result
            x -= 1
            y -= 1
    return result


def header(article):

    text = article.body
    root = etree.XML(text, etree.HTMLParser())
    raw_header = ''
    result_header = ''
    possible_lcs = []
    for d in root.iter():
        # case for sovsport, izvestia. rbc, ria, kp  ng;
        # meduza - name of newspaper is there
        # kommersant - the second entry is perfect, the first with name of the newspaper
        if d.tag == 'meta':
            for attr in d.attrib:
                if 'title' in d.attrib[attr]:
                    raw_header = d.attrib['content']
        # search for lcs in the content to delete name of newspaper
        if d.tag == 'div' or d.tag == 'h1' or d.tag == 'h2':  # maybe add some other tags for other newspapers
            for child in d:
                if child.text is not None:
                    possible_lcs.append(lcs(child.text, raw_header))
    # the longest from all lcs -- perfect header
    max_length = max(len(s) for s in possible_lcs)
    for string in possible_lcs:
        if len(string) == max_length:
            result_header = string
    return result_header