__author__ = 'Sereni'

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from newspaper.items import Article


class RbcSpider(CrawlSpider):
    name = 'rbc'
    allowed_domains = ['rbcdaily.ru']
    start_urls = [
        'http://rbcdaily.ru'
    ]
    rules = (
        Rule(LinkExtractor(allow='/2014/11/2[0-9]'), callback='parse_link',
             follow=True),  # should extract Nov 20-29
    )

    def parse_link(self, response):

        article_tracker = set([])
        paths = [
            '//a[@class="content__title-link"]',
            '//span[@class="preview-article-illustrated__title"]',
            '//a[@class="article-top__title-link"]',
            '//a[@class="preview-article__title-link"]'
        ]
        for path in paths:
            article_tracker = self.process_element(response, path, article_tracker)

    def process_element(self, response, path, articles):
        for item in response.xpath(path):
            title = item.xpath('./text()').extract()[0]
            try:
                link = item.xpath('./@href').extract()[0]
            except IndexError:  # text is in a child element
                link = item.xpath('../@href').extract()[0]

            if (title, link) not in articles:
                articles.add((title, link))

                article = Article(title=title, url=response.url + link)
                print article['title'], article['url']
        return articles