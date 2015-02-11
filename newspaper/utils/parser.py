# coding=utf-8
__author__ = 'Sereni'


def cyr(s):
    """Checks if a string has at least one cyrillic char"""

    # if decoding successful, no unicode -- bad string
    try:
        s.decode('ascii')
        return False

    # if decoding failed, unicode present -- may be a good string for now
    except UnicodeEncodeError:
        return True


def get_first(l):
    """Useful for getting the first item from extract()"""
    try:
        return l[0]
    except IndexError:
        return ''


def is_script(s):
    """Determines if string is a script rather than natural text"""
    # todo if forbidding scripts by tag won't do for some reason, write this out
    # no cyrillic text?
    # too much punctuation?
    pass


# I can't believe I have to write this out myself
def get_path(item):
    """Get path to a given node"""

    path = []

    # so I got desperate trying to put this into a list comprehension
    for ancestor in item.xpath('./ancestor::node()')+[item]:
        tag = get_first(ancestor.xpath('name(.)').extract())

        if ancestor.xpath('./@class').extract():
            attr = '[@class="{0}"]'.format(get_first(ancestor.xpath('./@class').extract()))
        else:
            attr = ''

        path.append(tag+attr)

    return '/' + '/'.join(path)


# it's probably irrelevant. maybe should just get parent path and quit
def get_common_path(node):
    """
    This is supposed to find the most usable path to a collection of nodes
    Since each node is scored by the text length in its siblings,
    we want to first get the parent node that contains all of them
    and then the highest possible node that contains that parent
    node and an arbitrary number of empty nodes
    """
    parent = node.xpath('./..')
    while True:
        texts = [text for text in parent.xpath('./child::*/text()') if text]

        if len(texts) > 1:
            parent = parent.xpath('./..')
        else:
            break

    # ah drop it, useless
    pass


def sibling_text_len(node):
    """
    Select the given node and all its siblings that have the same tag
    Return the total length of their text split by spaces
    """
    # get current node name
    node_name = node.xpath('name(.)').extract()[0]

    # select all nodes of node's parent that are the same tag as node
    # get their text, join it with spaces
    text = ' '.join([n.extract() for n in node.xpath('./../*[self::{0}]/text()'.format(node_name))])
    return len(text.split(' '))


def expand(node):
    # смотреть, есть ли у узла descendants из разрешённых тегов, у которых нет больше детей
    # если да, то их текст присобачить к тексту узла
    # из-за этого в дивах высокого уровня появится мусор: вот у тебя есть див, а где-то дофига внизу есть
    # маленький текстик в em, и он прибавится
    # надежда на то, что у высокого дива самого по себе нет текста, и тогда наверх всплывут только параграфы
    pass


def find_text(article):

    # get all nodes that have text
    # checking for cyrillic isn't great, the scripts often have cyrillic comments
    nodes = [n for n in article.xpath('//text()/..') if cyr(n.xpath('./text()').extract()[0]) and
             not n.xpath('name(.)').extract()[0] == 'script']  # assume no more scripts

    # split by whitespace: crude, sufficient.
    # longest = sorted(nodes, key=lambda x: len(x.xpath('./text()').extract()[0].split(' '))).pop()

    # for each node, assign a joint sibling text length, sort the nodes by this number, return the biggest
    longest = sorted(nodes, key=lambda x: sibling_text_len(x)).pop()

    return get_path(longest.xpath('./..'))


def find_title(article):
    pass


def find_date(article):
    pass


def find_author(article):
    pass

# rbc, sovsport and izvestia work like a charm
# fixme ria возвращает правила комментирования -- смешно конечно, но неполезно
