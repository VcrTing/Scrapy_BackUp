# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

import os

BASE_DIR = os.path.dirname(__file__)

class NewaveItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 大分类/母分类
    mainType = scrapy.Field()
    # 母分类子类
    childType = scrapy.Field()

    # 母文件夹名
    mainFile = scrapy.Field()
    # 子文件夹名
    childFile = scrapy.Field()

    # 子分类帖子的标题
    itemTitle = scrapy.Field()
    # 子分类帖子的url
    itemUrl = scrapy.Field()

    # 帖子文件夹名
    itemFile = scrapy.Field()
    # 帖子内容
    content = scrapy.Field()