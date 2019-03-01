# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst

from .tools import remove_ntr, remove_ntr_re

class Fk5378Item(scrapy.Item):
    sys_item = scrapy.Field()
    rsc_item = scrapy.Field()
    save_path = Field(
        input_processor = MapCompose(remove_ntr),
    )

class SysItem(scrapy.Item):
    spider_start_time = scrapy.Field()    # （爬虫启动北京时间 年月日时分秒）
    spider_use_time = scrapy.Field()      # （爬取使用时间 unix时间戳）
    pipeline_use_num = scrapy.Field()     # （爬虫经过pipeline的次数）

class RSCItem(scrapy.Item):
    # 标题
    # 时间长短
    # 上传日期
    # 包含的标签
    # 封面
    # 观看人数
    # 作者
    # 帖子链接
    # 视频下载链接
    title = Field(
        input_processor = MapCompose(remove_ntr_re),
    )
    time_num = scrapy.Field()
    publish_date = scrapy.Field()
    tags = scrapy.Field()
    cover = scrapy.Field()
    see_num = scrapy.Field()
    author = scrapy.Field()
    item_url = scrapy.Field()
    vedio_url = scrapy.Field()
