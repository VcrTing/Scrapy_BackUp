# -*- coding: utf-8 -*-
import re
import os
import json
import time
import shutil
import datetime

import codecs
import requests
from .settings import BASE_DIR
from .tools import dir_maker, remove_item_re, remove_ntr_re, get_ch

# Original
class Fk5378Pipeline(object):
    def process_item(self, item, spider):
        return item

# Disk txt file
class PathPipeline(object):
    def __init__(self):
        self.file = None

    def process_item(self, item, spider):
        sys_item = eval(item['sys_item'])
        rsc_item = eval(item['rsc_item'])

        # CLEANER
        for k,v in rsc_item.items():
            rsc_item[k] = remove_ntr_re(v)
        rsc_item['tags'] = get_ch(rsc_item.get('tags'))

        # BUILD
        _data = {
            '爬虫作者': '曾影穹(vcrting@163.com)'
        }
        for k in rsc_item:
            _data[k] = rsc_item[k]
        for k in sys_item:
            _data[k] = sys_item[k]
        data_str = json.dumps(_data, ensure_ascii=False)

        # PATH
        save_path = os.path.join(item['save_path'], rsc_item['title'])
        if dir_maker(save_path):
            # FILE
            self.file = codecs.open(
                os.path.join(
                    save_path,
                    rsc_item['title'] + '.json'
                ), 
                'wb', 
                encoding='utf-8'
            )
            self.file.write(data_str)
            
            # IMG
            image = requests.get(rsc_item['cover']).content 
            image_save_path = os.path.join(
                save_path,
                rsc_item['title'] + '_' + rsc_item['cover'][-6:]
            )
            with open(image_save_path, 'wb') as f:
                f.write(image)
                
        return item

    def close_spider(self, spider):
        self.file.close()
