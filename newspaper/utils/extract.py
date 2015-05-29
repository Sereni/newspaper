__author__ = 'Sereni'


def text(response, xpath):
    """
    Given a response and an xpath, get text inside xpath separated with <p> tags
    """
    article_text = ''

    # get everything inside xpath tag
    nodes = response.xpath(xpath)

    for node in nodes:

        # get node tag to filter randomness. hm, this might break
        name = node.xpath('name(.)').extract()[0]
        if name == 'p' or name == 'div':

            # get text of node and its descendants, write between <p>s and append to text
            article_text = article_text + '<p>{0}</p>\n'.format(node.xpath("string(.)").extract())

    return article_text


def year_month(s):
    """
    Given item's date in some fixed format, return year and month to use in folder names
    """
    pass