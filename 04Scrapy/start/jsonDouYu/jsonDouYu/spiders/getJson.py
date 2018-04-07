# -*- coding: utf-8 -*-
import scrapy
from jsonDouYu.items import JsondouyuItem
import json,demjson

class GetjsonSpider(scrapy.Spider):
    name = 'getJson'
    allowed_domains = ['capi.douyucdn.cn/api/v1/getVerticalRoom']
    limit = 20
    offset = 1
    url = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom/'
    start_urls = [url+'?limit='+str(limit)+'&offset='+str(offset)]

    def parse(self, response):
        offset = 1
        while True:
            print(self.url+'?limit='+str(self.limit)+'&offset='+str(offset),callback=self.parse())
            if offset >= 200 :
                break
            #把json转为python, data是列表
            data = []
            data = json.loads(response.text)
            print(data)
            for each in data['data'] :
                item = JsondouyuItem()
                item['nickName'] = each['nickname']
                item['roomId'] = each['room_id']
                item['roomName'] = each['room_name']
                item['picUrl'] = each['vertical_src']
                item['gameName'] = each['game_name']
                item['anchorCity'] = each['anchor_city']

                yield item

            offset += 1
            yield scrapy.Request(self.url+'?limit='+str(self.limit)+'&offset='+str(offset),callback=self.parse)
