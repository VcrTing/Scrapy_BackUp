# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import Rule,CrawlSpider
from scrapy.linkextractors import LinkExtractor

from sun0769.items import boxItem,messageItem

class SunSpider(CrawlSpider):
    name = 'sun'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/report?page=']

    pageLink = LinkExtractor(allow='report')#获取分页链接
    contentLink = LinkExtractor(allow=r'/html/question/\d+/\d+.shtml')#获取帖子链接并跟入，然后进行爬取
    rules = [
        Rule(pageLink,process_links='itemLinks'),
        Rule(contentLink,callback='parseMessage')
    ]

    def parseMessage(self,response):
        msg = messageItem()
        msgTopTitle = response.xpath('//div[@class="pagecenter p3"]/div[1]/div[1]/div/strong/text()').extract()[0]

        # 帖子Id
        msg['itemId'] = msgTopTitle.split(' ')[-1].split(':')[-1]
        # 帖子标题
        msg['msgTitle'] = msgTopTitle
        print(msg['msgTitle'])
        # 帖子内容面，有图片
        content = response.xpath('//div[@class="contentext"]/text()').extract()
        if len(content) == 0:
            content = response.xpath('//div[@class="c1 text14_2"]/text()').extract()
            msg['msgContent'] = ''.join(content).strip()
        else :
            msg['msgContent'] = ''.join(content).strip()
            # 帖子图片地址,例子：http://wz.sun0769.com/uploads/attached/2018/03/62e759bd6f5ce2b2d1af54f4d214106c.jpg
            imgUrl = response.xpath('//div[@class="textpic"]/img/@src').extract()[0]
            if str(imgUrl).find('http') == -1:
                msg['msgImgUrl'] = 'http://wz.sun0769.com' + str(imgUrl)
        # 处理状态
        msg['msgStatus'] = response.xpath('//div[@class="audit"]/div/span/text()').extract()[0]

        yield msg

'''
    def parseItem(self, response):
        for each in response.xpath('//*[@id="morelist"]/div/table[2]/tr/td/table/tr'):
            box = boxItem()
            # 编号
            box['itemId'] = each.xpath('./td[1]/text()').extract()[0]
            # 类型
            box['itemType'] = each.xpath('./td[2]/a[1]/text()').extract()[0]
            # 标题
            box['itemTitle'] = each.xpath('./td[2]/a[2]/text()').extract()[0]
            # 地址
            box['itemAddr'] = each.xpath('./td[2]/a[3]/text()').extract()[0]
            # 帖子状态
            box['itemStatus'] = each.xpath('./td[3]/span/text()').extract()[0]
            # 投诉的网友名
            box['itemPeople'] = each.xpath('./td[4]/text()').extract()[0]
            # 帖子发布时间
            box['itemTime'] = each.xpath('./td[5]/text()').extract()[0]

            yield box
'''