# -*- coding: utf-8 -*-
import scrapy
from newave.items import NewaveItem
from newave.items import BASE_DIR
import os,time,logging,re,datetime

class GetSpider(scrapy.Spider):
    name = 'get'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']
    i = 0
    j = 0

    def parse(self, response):
        dataPath = os.path.join(BASE_DIR,'data')
        if not os.path.exists(dataPath) :
            os.makedirs(os.path.join(BASE_DIR,'data'))

        for mainTypeT in response.xpath('//*[@id="tab01"]/div[@class="clearfix"]'):
            mainTextList = mainTypeT.xpath('./h3[@class="tit02"]/a/text() | ./h3[@class="tit02"]/span/text()').extract()

            childLinkList = mainTypeT.xpath('./ul[@class="list01"]/li/a/@href').extract()
            childTextList = mainTypeT.xpath('./ul[@class="list01"]/li/a/text()').extract()

            childLinkAll = []
            item = []
            for mt in mainTextList :
                mainPath = os.path.join(dataPath,mt)
                if not os.path.exists(mainPath) :
                    os.makedirs(mainPath)

                for ci in range(0, len(childTextList)) :
                    childPath = os.path.join(mainPath,childTextList[ci])
                    if not os.path.exists(childPath) :
                        os.makedirs(childPath)

                    items = NewaveItem()
                    items['mainType'] = mt
                    items['mainFile'] = mainPath
                    items['childType'] = childTextList[ci]
                    items['childFile'] = childPath
                    self.j += 1
                    childLinkAll.append(childLinkList[ci])
                    item.append(items)

            for cl in range(0, len(childLinkAll)) :
                yield scrapy.Request(childLinkAll[cl], meta = {'items': item[cl]},callback = self.parseItem)

            print('j = '+str(self.j))

    def parseItem(self,response):
        itemUrl = []

        # 爬取页面所有a标签
        for each in response.xpath('//a') :
            allLink = each.xpath('./@href').extract()
            # 选取url
            for al in allLink :
                if str(response.url).split('/')[2] in al :
                    if al[-6:] == '.shtml' :
                        itemUrl.append(al)

        # 发送帖子url
        for il in range(0, len(itemUrl)):
            items = response.meta['items']
            items['itemUrl'] = itemUrl[il]                                 # 保存url
            yield scrapy.Request(itemUrl[il], meta={'item': items}, callback=self.parseContent)

    def parseContent(self,response) :
        item = response.meta['item']
        self.i += 1
        print('i = '+ str(self.i))

        title = response.xpath('//h1/text()').extract()
        allText = response.xpath('//div[@class!="footer"]/p/text()').extract()
        dataTime = response.xpath('//span[@class="date"]/text() | //span[@class="pull-date"]/text() '
                                  '| //span[@class="pub-date"]/text() | //span[@class="time-source"]/text()').extract()

        dataTime = [x for x in dataTime if x != ' ']
        if len(dataTime) == 0 :
            dataTime = datetime.datetime.today()
        item['itemTitle'] = ','.join(x for x in title if x != ' ')
        item['content'] = '\n'.join(x for x in allText if x != ' ')
        item['itemFile'] = str('['+str(dataTime)+ ']' + item['itemTitle']).replace(r'\n','').replace(r'\t','').replace('\\','')

        yield item
