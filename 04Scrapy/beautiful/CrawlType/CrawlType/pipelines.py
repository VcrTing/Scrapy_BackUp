# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class TencentinfoPipeline(object):

    def __init__(self):
        self.file_name = open('tencent.json','wb')
        print('='*40)

    def process_item(self, item, spider):
        print('>'*40)
        #写入数据
        jsontext = json.dumps(dict(item),ensure_ascii = False)+'\n'
        self.file_name.write(jsontext.encode(encoding='utf-8'))

        return item

    def close_spider(self,spider):
        self.file_name.close()
        print('<'*40)