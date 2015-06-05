# coding=utf-8
__author__ = 'Sereni'
from lxml import etree

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


def sibling_text(node):
    """
    Select the given node and all its siblings that have the same tag
    Return their joint text
    """
    # get current node name
    node_name = node.xpath('name(.)').extract()[0]

    # select all nodes of node's parent that are the same tag as node
    # get their text, join it with spaces
    text = ' '.join([n.extract() for n in node.xpath('./../*[self::{0}]/text()'.format(node_name))])
    return text


def find_text(article):

    # get all nodes that have text
    # checking for cyrillic isn't great, the scripts often have cyrillic comments
    nodes = [n for n in article.xpath('//text()/..') if cyr(n.xpath('./text()').extract()[0]) and
             not n.xpath('name(.)').extract()[0] == 'script']  # assume no more scripts

    # split by whitespace: crude, sufficient.
    # longest = sorted(nodes, key=lambda x: len(x.xpath('./text()').extract()[0].split(' '))).pop()

    # ~~~~~ the old individual version starts here

    # # for each node, assign a joint sibling text length, sort the nodes by this number, return the biggest
    # longest = sorted(nodes, key=lambda x: len(sibling_text(x).split(' '))).pop()
    #
    # return get_path(longest.xpath('./..'))

    # ~~~~~ the pipeline version starts here

    # for each node, record its sibling text and node xpath, sort by joint text length
    texts = sorted(list(set([(sibling_text(node), get_path(node.xpath('./..'))) for node in nodes])),
                   key=lambda x: len(x[0].split(' ')))
    # ok, I'm making it a set to remove duplicates on one page, and then back to list to sort it
    # for instance, the article is stored as many times as there are paragraphs in it, see how sibling-text works
    # this is real important for the pipeline to work, please don't remove

    return texts


def capitalized(s):
    """
    Check if a string starts with a capital letter
    """
    if s[0].lower() == s[0]:
        return False
    return True


def find_author(article):
    # select nodes the attributes of which have 'author' in them
    # check their text value: the first two words should be capitalized

    authors = []
    root = etree.XML(article.body.decode('utf-8'), etree.HTMLParser())
    for e in root.iter():
        for a in e.attrib:
            if 'author' in e.attrib[a]:
                if e.text:
                    words = e.text.split()
                    if len(words) > 1 and capitalized(words[0]) and capitalized(words[1]):
                        authors.append(' '.join(words))

    # nothing works, so meh, let's use lxml
    # nodes = [n.extract() for n in article.xpath('//*/@*[contains(name(), "author")]/..')]
    #          # if len(n.extract().split(' ')) > 1
    #          # and capitalized(n.extract().split(' ')[0])
    #          # and capitalized(n.extract().split(' ')[1])]

    return authors


# these two are implemented for each individual response in extract.py
def find_title(article):
    pass


def find_date(article):
    pass


