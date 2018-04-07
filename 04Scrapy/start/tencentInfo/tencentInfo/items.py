# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentinfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #职位
    name = scrapy.Field()
    #详情链接
    link = scrapy.Field()
    #招聘类别
    type = scrapy.Field()
    #工作地点
    addr = scrapy.Field()
    #招牌人数
    peopleNum = scrapy.Field()
    #发布时间
    publishTime = scrapy.Field()