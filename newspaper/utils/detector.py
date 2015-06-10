# coding=utf-8
__author__ = 'Sereni'
"""
This module doesn't do anything in the production
Kept for code snippets mostly, may be safely deleted
"""
# given a newspaper start page, give out a url pattern for articles
# let's assume you're getting a response from spider already, so it's html
# parse html, find large chunks of text
# near those chunks, you'll have multi-word link texts, the actual links are probably articles

# стратегии

# /done/ 1. sov, izv, rbc: найти длинный блок текста. в одном из предыдущих сиблингов искать <a> с 2+ словами (рекурсивно) href достать.
# до этого сиблинга, бывает, надо подняться на 1-2 уровня
# /done/ 2. если много текста в <a>, копируй href оттуда -- они продублированы
# 3. Параллельно: бывают заголовки без превью. они в <a>, обычно . нужны ограничения на хреф: тот же домен
# как быть с авторскими колонками и прочей дрянью?


def find_links(response):
    # find text() nodes longer than, say, 20 words divided by spaces -- these are article previews
    # mind that these are nodes, not actual text (which is good)

    print '~'*5 + 'called the detector'

    previews = [text for text in response.xpath('//text()') if len(text.extract()[0].split()) > 20]
    links = []

    # now we wanna process this stuff
    for node in previews:

        # first, check if the node has a href associated with it -- if it does, this is the article link
        self_link = node.xpath('./@href')
        if self_link:
            links.append(self_link)

        # look for previous siblings that are <a> with 2+ words
        # allow to rise for 2 levels of depth to account for divs (if false positives, look here)
        depth = 0
        while depth < 3:
            lift = '../'

            # find all <a> nodes above the long text, up to 2
            link_nodes = node.xpath('./{0}preceding-sibling::node/descendant-or-self::a'.format(lift * depth))
            new_links = [n.xpath('/@href').extract()[0] for n in link_nodes if n.xpath('/text()').extract()[0]
                         .split() > 2]  # there are a lot of 2-word titles, but also a lot of trash

            # will only go up a level if nothing found on this level. hopefully not that often.
            if new_links:
                links += new_links
                break
            depth += 1
    print set(links)
    return links


def extrapolate(links):
    # not too general though
    pass