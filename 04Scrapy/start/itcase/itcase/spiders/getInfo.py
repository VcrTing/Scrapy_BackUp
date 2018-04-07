# -*- coding: utf-8 -*-
import scrapy
from itcase.items import ItcaseItem

class GetinfoSpider(scrapy.Spider):
    name = 'getInfo'
    allowed_domains = ['www.itcast.cn/channel/teacher.shtml#apython']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml#apython/']

    def parse(self, response):
        list_info = response.xpath('//div[@class="li_txt"]')
        teacherItem = []

        for each in list_info:
            item = ItcaseItem()
            name = each.xpath('./h3/text()').extract()
            title = each.xpath('./h4/text()').extract()
            info = each.xpath('./p/text()').extract()

            item['name'] = name[0]
            item['title'] = title[0]
            item['info'] = info[0]

            yield item
