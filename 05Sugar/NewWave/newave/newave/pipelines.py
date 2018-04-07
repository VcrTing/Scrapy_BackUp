# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs,os

class NewavePipeline(object):
    def __init__(self):
        self.f = None

    def process_item(self, item, spider):
        childFile = item['childFile']
        itemFile = item['itemFile']
        print('-'*80)
        print('File = '+ str(os.path.join(childFile, itemFile + '.txt')))

        content = []
        '''
        cList = item['content'].split('。')
        if cList :
            for i in cList :
                i = i + '。\n'
                content.append(i)
        else :
            content = ['None']'''
        con = item['content'] + '\n\n' + item['itemUrl']
        self.f = codecs.open(os.path.join(childFile, itemFile + '.txt'),'w' ,encoding = 'utf-8')
        self.f.write(con)

        return item

    def close_spider(self,spider):
        self.f.close()
