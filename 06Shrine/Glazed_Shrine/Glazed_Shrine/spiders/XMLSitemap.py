# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

#琉璃神社's XMLSitemap
class XMLSitemapSpider(CrawlSpider):
    name = 'XMLSitemap'
    allowed_domains = ['www.llss.pw']
    start_urls = ['https://www.llss.pw/wp/sitemap.html']

    rules = [
        Rule(LinkExtractor(allow = r'/wp/[a-zA-Z0-9_-]+.html')
             ,callback = 'parse_url',follow = True),
    ]

    def parse_url(self,response):
        '''
        此爬虫会经过的第一个解析方法，用于解析sitemap.html页面的url，并跟进url
        :param response:
        :return:
        '''
        yield scrapy.Request( url = response.url, callback = self.parse_url_in)

    def parse_url_in(self, response):
        print('url = '+response.url)
