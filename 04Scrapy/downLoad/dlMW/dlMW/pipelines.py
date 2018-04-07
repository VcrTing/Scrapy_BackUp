# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

class DlmwPipeline(object):
    def __init__(self,mongo_host,mongo_port,mongo_dbName,mongo_docName):
        #定义MongoDB连接数据
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_dbName = mongo_dbName
        self.mongo_docName = mongo_docName
        #定义其他功能要用的东西
        pass

    #用于访问Settings
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_host=crawler.settings.get('MONGODB_HOST'),
            mongo_port=crawler.settings.get('MONGODB_PORT'),
            mongo_dbName=crawler.settings.get('MONGODB_DBNAME'),
            mongo_docName=crawler.settings.get('MONGODB_DOCNAME')
        )

    def open_spider(self,spider):
        #打开为MongoDB存储
        self.client = pymongo.MongoClient(host=self.mongo_host,port=self.mongo_port)
        self.db = self.client[self.mongo_dbName]

    def process_item(self, item, spider):
        # 存储mongodb
        table = self.db[self.mongo_docName]
        table.insert(dict(item))

        return item

    def close_spider(self, spider):
        self.client.close()