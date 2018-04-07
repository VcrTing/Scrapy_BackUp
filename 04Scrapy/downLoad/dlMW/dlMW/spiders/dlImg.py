# -*- coding: utf-8 -*-
import scrapy
from dlMW.items import DlmwItem

class DlimgSpider(scrapy.Spider):
    name = 'dlImg'
    allowed_domains = ['movie.douban.com']
    offset = 0
    url = 'http://movie.douban.com/top250?start='
    start_urls = [url+str(offset),]

    def parse(self, response):
        item = DlmwItem()
        for each in response.xpath('//div[@class="info"]'):
            item['title'] = each.xpath('.//span[@class="title"][1]/text()').extract()[0]
            item['star'] = each.xpath('.//div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
            quote = each.xpath('.//p[@class="quote"]/span/text()').extract()
            if quote :
                item['quote'] = quote[0]
            else :
                item['quote'] = quote

            yield item
        if self.offset < 25 :
            self.offset += 25
            yield scrapy.Request(self.url+str(self.offset),callback=self.parse)