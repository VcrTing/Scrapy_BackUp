# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json,os
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from jsonDouYu.settings import *
from scrapy.exceptions import DropItem

img_path = os.path.join(BASE_DIR,'img')

class JsondouyuPipeline(ImagesPipeline):
    IMAGES_STORE = Settings().get('IMAGES_STORE')

    def get_media_requests(self, item, info):
        image_url = item['picUrl']
        print('Here is image_url = '+str(image_url))
        yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        new_name = os.path.join(img_path,image_path[0][:10]+item['nickName']+item['roomId']+'.jpg')
        #os.renames(os.path.join(img_path,image_path[0]), new_name)
        item['imagePath'] = image_path[0]
        return item