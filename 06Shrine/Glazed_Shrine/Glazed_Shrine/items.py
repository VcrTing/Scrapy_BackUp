# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy,os

BASE_DIR = os.path.dirname(__file__)

class GlazedShrineItem(scrapy.Item):

    #帖子
    itemItem = scrapy.Field()
    #资源
    rscItem = scrapy.Field()
    #图片
    imgItem = scrapy.Field()
    #系统
    scrapyItem = scrapy.Field()

class ItemItem(scrapy.Item):

    item_title = scrapy.Field()           # （帖子标题）
    item_content = scrapy.Field()         # （帖子内容）
    item_url = scrapy.Field()             # （帖子网站地址）
    save_path = scrapy.Field()            # （该资源储存的文件夹地址）
    item_type = scrapy.Field()            # （资源类别，例子：动画）
    comment_num = scrapy.Field()          # （评论数量）
    item_time = scrapy.Field()            # （帖子时间）
    item_author = scrapy.Field()          # （发帖人）

class RSCItem(scrapy.Item):

    rsc_msg_all = scrapy.Field()          # （资源的所有信息）
    ratings_num = scrapy.Field()          # （资源评分值）
    down_addr = scrapy.Field()            # （资源下载地址）

class ImageItem(scrapy.Item):

    img_item_url = scrapy.Field()         # （帖子图片url）
    img_rsc_url = scrapy.Field()          # （资源内景图片url，多个图片则用’，‘中文逗号分割组成字符串）
    img_path = scrapy.Field()             # （图片的保存地址）

class ScrapyItem(scrapy.Item):

    spider_start_time = scrapy.Field()    # （爬虫启动北京时间 年月日时分秒）
    spider_use_time = scrapy.Field()      # （爬取使用时间 unix时间戳）
    pipeline_use_num = scrapy.Field()     # （爬虫经过pipeline的次数）