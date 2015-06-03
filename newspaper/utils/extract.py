__author__ = 'Sereni'

import re

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
        if name == 'p' or name == 'div':
# fixme all p's are squished into one, should be more
# testing: if I leave out a \r\n, do the line breaks change in the file? is this the place to insert the tag?
# if yes, why the heck is there just one tag and so many line breaks in between?
# might as well just replace two consecutive line breaks with one line break and a </p><p> when text is assembled.
            # get text of node and its descendants, write between <p>s and append to text
            # print ' '.join(node.xpath("string(.)").extract()).replace('\r', '~~~~').replace('\n', '~~~~')
            text = re.sub('(\n)+', '</p><p>', ' '.join(node.xpath("string(.)").extract()))
            # article_text = article_text + u'<p>{0}</p>\r\n'.format \
            #     (' '.join(node.xpath("string(.)").extract()).replace('\n', '</p><p>'))
            article_text = article_text + u'<p>{0}</p>\r\n'.format(text)

    return article_text


def year_month(s):
    """
    Given item's date in some fixed format, return year and month to use in folder names
    """
    pass