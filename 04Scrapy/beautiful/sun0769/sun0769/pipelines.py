# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs

class Sun0769Pipeline(object):
    def process_item(self, item, spider):
        return item

class BoxPipeline(object):
    def __init__(self):
        self.fileName = ['阳光东莞问政：'+str(x)+'.json' for x in range(1,6)]#定义文件存储名
        self.saveNum = 200#限定一个存储200条帖子
        self.i = 0#控制files列表的变量
        self.offset = 0#控制saveNum的变量
        self.files = []#File对象

    def open_spider(self,spider):
        for x in self.fileName:
            self.files.append(codecs.open(x,'w',encoding='utf-8'))

    def process_item(self, item, spider):
        if str(item.__class__) != "<class 'sun0769.items.boxItem'>":
            return item

        jsonText = json.dumps(dict(item),ensure_ascii=False)+'\n'

        self.offset = self.offset + 1
        if self.offset >= self.saveNum:
            self.i = self.i + 1
            self.offset = 0

        jbFile = self.files[self.i]
        jbFile.write(jsonText)

        return item

    def close_spider(self,spider):
        for x in self.files:
            x.close()

class MessagePipeline(object):
    def __init__(self):
        self.fileName = ['帖子：'+str(x)+'.json' for x in range(1,6)]#定义文件存储名
        self.saveNum = 200#限定一个存储200条帖子
        self.i = 0#控制files列表的变量
        self.offset = 0#控制saveNum的变量
        self.files = []#File对象

    def open_spider(self,spider):
        for x in self.fileName:
            self.files.append(codecs.open(x,'w',encoding='utf-8'))

    def process_item(self, item, spider):
        if str(item.__class__) != "<class 'sun0769.items.messageItem'>":
            return item

        jsonText = json.dumps(dict(item),ensure_ascii=False)+'\n'

        self.offset = self.offset + 1
        if self.offset >= self.saveNum:
            self.i = self.i + 1
            self.offset = 0

        jbFile = self.files[self.i]
        jbFile.write(jsonText)

        return item

    def close_spider(self,spider):
        for x in self.files:
            x.close()