# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JsondouyuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nickName = scrapy.Field()
    roomId = scrapy.Field()
    roomName = scrapy.Field()
    picUrl = scrapy.Field()
    imagePath = scrapy.Field()
    gameName = scrapy.Field()
    anchorCity = scrapy.Field()
