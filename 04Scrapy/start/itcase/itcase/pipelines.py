# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class ItcasePipeline(object):
    def __init__(self):
        #初始化文件
        self.file_name = open('teacher.json','wb')

    def open_spider(self,spider):
        print('-'*40+'tag'+'-'*40)

    def process_item(self, item, spider):
        #写入数据
        jsontext = json.dumps(dict(item),ensure_ascii = False)+'\n'
        self.file_name.write(jsontext.encode(encoding='utf-8'))

        return item

    def close_spider(self,spider):
        #关闭文件
        self.file_name.close()