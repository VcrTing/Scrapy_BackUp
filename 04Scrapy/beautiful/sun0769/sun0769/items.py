# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Sun0769Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class boxItem(scrapy.Item):
    #编号
    itemId = scrapy.Field()
    #类型
    itemType = scrapy.Field()
    #标题
    itemTitle = scrapy.Field()
    #地址
    itemAddr = scrapy.Field()
    #帖子状态
    itemStatus = scrapy.Field()
    #投诉的网友名
    itemPeople = scrapy.Field()
    #帖子发布时间
    itemTime = scrapy.Field()

class messageItem(scrapy.Item):
    #对应的帖子id
    itemId = scrapy.Field()
    #帖子标题
    msgTitle = scrapy.Field()
    #帖子图片地址
    msgImgUrl = scrapy.Field()
    #帖子内容
    msgContent = scrapy.Field()
    #处理状态
    msgStatus = scrapy.Field()