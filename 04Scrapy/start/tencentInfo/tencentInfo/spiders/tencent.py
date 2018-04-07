                                                     # -*- coding: utf-8 -*-
import scrapy
from tencentInfo.items import TencentinfoItem

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    url = 'https://hr.tencent.com/position.php?&start='
    offset = 0#偏移量

    start_urls = [url+str(offset)]

    def parse(self, response):
        for each in response.xpath('//tr[@class="even"] | //tr[@class="odd"]'):
            #初始化模型对象
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

            yield tcInfo

        #再度请求，要用yield
        if self.offset < 1000:
            self.offset += 10
        else:
            raise '结束工作！！！'
        yield scrapy.Request(self.url+str(self.offset), callback=self.parse)
