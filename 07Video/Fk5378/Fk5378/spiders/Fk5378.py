import os
import re
import time

import scrapy 
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

from Fk5378.items import Fk5378Item, RSCItem, SysItem
from ..settings import BASE_DIR, URL_RECORD_FILE, DATA_SAVE_DIR
from ..tools import remove_ntr, remove_item, FindError

# www.fk5378.com
class Fk5378Spider(CrawlSpider):
    name = 'Fk5378'
    base_url = 'https://www.fk5378.com'
    allowed_domains = ['www.fk5378.com']
    rules = [
        Rule(LinkExtractor(allow = r'page=\d+')
            ,callback = 'parse_page',follow = True
        ),
    ]

    pipeline_use_num = 0
    start_url = [
        'https://www.fk5378.com/tag/%E6%9C%AC%E5%9C%9F', # 本土
        'https://www.fk5378.com/tag/%E6%AD%A3%E5%A6%B9', # 正妹
        'https://www.fk5378.com/tag/%E5%AD%B8%E7%94%9F', # 学生
        'https://www.fk5378.com/tag/%E6%A8%A1%E7%89%B9', # 模特
        'https://www.fk5378.com/tag/%E5%B7%A8%E4%B9%B3'  # 巨乳
    ]
    spider_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def start_requests(self):
        """
            爬前准备
        """
        start_urls = []
        try:
            input('Hi, You Spider will be start!!!')
            start_urls.append(self.start_url[2])
        except:
            start_urls = self.start_url
        finally:
            dataPath = os.path.join(BASE_DIR, DATA_SAVE_DIR)
            if not os.path.exists(dataPath):
                os.makedirs(dataPath)
        for url in start_urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse_page(self, response):
        """
            爬取分页
        """
        soup = BeautifulSoup(response.body, 'lxml')
        gategory = soup.find('div', { 'class': 'body-content' }).find('h1').get_text()[-2:]
        print('gategory', gategory)
        for each in soup.find_all(class_='post-item'):
            try:
                next_url = self.base_url
                next_url +=  each.find('a').get('href')
            except Exception:
                raise FindError
            else:
                yield scrapy.Request(
                    url = next_url,
                    meta = {
                        'gategory': gategory
                    },
                    callback = self.parse_rsc
                )
    
    def parse_rsc(self, response):
        """
            爬取资源
        """
        rsc = RSCItem()
        sys = SysItem()
        fk5378 = Fk5378Item()

        self.pipeline_use_num += 1
        gategory = response.meta['gategory']

        soup = BeautifulSoup(response.body, 'lxml')

        rsc['cover'] = soup.find('video').get('poster')
        rsc['vedio_url'] = soup.find('source').get('src')
        rsc['title'] = soup.find('h1', { 'class': 'video-title', }).get_text()
        rsc['item_url'] = soup.find('meta', { 'property': 'og:url' }).get('content')

        rsc['tags'] = response.xpath('//div[@class="video-info"]/ul/li[1]//text()').extract()
        rsc['time_num'] = response.xpath('//div[@class="video-info"]/ul/li[2]/text()').extract()[0]
        rsc['publish_date'] = response.xpath('//div[@class="video-info"]/ul/li[3]/text()').extract()[0]

        rsc['author'] = soup.find('div', { 'class': 'video-info' }).find('ul').find_all('li')[3].get_text()
        rsc['see_num'] = soup.find('div', { 'class': 'video-info' }).find('ul').find_all('li')[4].get_text()

        sys['pipeline_use_num'] = self.pipeline_use_num
        sys['spider_use_time'] = self.spider_start_time
        sys['spider_start_time'] = self.spider_start_time

        publish_date_list = re.findall(r"\d+", remove_ntr(rsc['publish_date']))
        publish_date = publish_date_list[0] + '-' + publish_date_list[1]
        save_path = os.path.join(
            BASE_DIR,
            DATA_SAVE_DIR,
            gategory,
            publish_date
        )

        fk5378['rsc_item'] = str(rsc)
        fk5378['sys_item'] = str(sys)
        fk5378['save_path'] = save_path

        yield fk5378
