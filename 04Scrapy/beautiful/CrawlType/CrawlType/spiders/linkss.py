# -*- coding: utf-8 -*-
import scrapy
#导入链接规则匹配类
from scrapy.linkextractors import LinkExtractor
#导入CrawlSpider父类和Rule规则
from scrapy.spider import CrawlSpider,Rule
from CrawlType.items import TencentinfoItem

class LinkssSpider(CrawlSpider):
    name = 'linkss'#scrapy crawl linkss运行
    allowed_domains = ['hr.tencent.com']
    start_urls = ['http://hr.tencent.com/position.php']

    pageNum = 1

    link_page = LinkExtractor(allow=('start=\d+'))
    rules = [
        Rule(link_page,callback='parseTencent',follow=True)
        #,Rule(link_test,callback=)
    ]

    def parseTencent(self,response):
        #evenList = response.xpath('//tr[@class="even"]')
        #oddList = response.xpath('//tr[@class="odd"]')
        #fullList = evenList + oddList
        #for each in fullList:
        print('-'*40)
        for each in response.xpath('//tr[@class="even"] | //tr[@class="odd"]'):
            # 初始化模型对象
            tcInfo = TencentinfoItem()
            # 职位
            tcInfo['name'] = each.xpath('./td[1]/a/text()').extract()[0]
            # 详情链接
            tcInfo['link'] = each.xpath('./td[1]/a/@href').extract()[0]
            # 招聘类别
            tcInfo['type'] = each.xpath('./td[2]/text()').extract()
            # 工作地点
            tcInfo['addr'] = each.xpath('./td[3]/text()').extract()[0]
            # 招牌人数
            tcInfo['peopleNum'] = each.xpath('./td[4]/text()').extract()[0]
            # 发布时间
            tcInfo['publishTime'] = each.xpath('./td[5]/text()').extract()[0]

            #Break
            self.pageNum = self.pageNum + 1
            if self.pageNum >= 10:
                print(self.pageNum)
                break

            yield tcInfo#有这个，scrapy才会调用pipeline里面的process_item方法
