# -*- coding: utf-8 -*-
import scrapy,os,time,datetime,shutil,json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from Glazed_Shrine.items import GlazedShrineItem,ItemItem,RSCItem,ImageItem,ScrapyItem,BASE_DIR
from bs4 import BeautifulSoup

#琉璃神社
class GlazedshrineSpider(CrawlSpider):
    name = 'GlazedShrine'
    allowed_domains = ['www.llss.pw']
    spider_start_time = datetime.datetime.now()
    fileDir = 'DATA_SAVE'
    pipeline_use_num = 0
    custom_settings = {
        'ITEM_PIPELINES': {
            'Glazed_Shrine.pipelines.PathShrinePipeline':400,
            #'Glazed_Shrine.pipelines.MysqlShrinePipeline':500,
        }
    }
    start_urls = ['https://www.llss.pw/wp/anime.html',#动画
                  'https://www.llss.pw/wp/comic.html',#动漫
                  'https://www.llss.pw/wp/game.html',#游戏
                  'https://www.llss.pw/wp/book.html',#小说
                  'https://www.llss.pw/wp/age.html'#壁纸/文章
    ]

    rules = [
        Rule(LinkExtractor(allow = r'/page/\d+')
             ,callback = 'parse_page',follow = True),
    ]

    def start_requests(self):
        '''
        在第一个请求开始之前，让用户选择要爬取的内容
        :return:start_urls
        '''
        start_urls = []

        try:
            thing = int(input('你想爬取琉璃神社的哪类数据？请选择输入[1、动画，2、漫画，3、游戏，4、小说，5、壁纸/文章，6、全部]中的一个数字：'))
            start_urls.append(self.start_urls[thing-1])
        except Exception :
            start_urls = self.start_urls
        for url in start_urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse_page(self,response):
        '''
        解析分页内的数据，即依据分页url解析帖子
        :param response:响应文件
        :return:item's url 和url
        '''
        dataPath = os.path.join(BASE_DIR, self.fileDir)
        if not os.path.exists(dataPath) :
            os.makedirs(dataPath)
        soup = BeautifulSoup(response.body,'lxml')
        now_page_num = soup.find('li',{'class':'active_page'}).get_text()
        for each in soup.find_all('article'):
            item = ItemItem()
            try :
                item['item_title'] = each.find('header').find('h1').find('a').get_text()                                                                                                        # （帖子标题）
                item['item_content'] = each.find('div',{'class':'entry-content',}).find('p').get_text()                                                                                         # （帖子内容）
                item['item_url'] = each.find('header').find('h1').find('a').get('href')                                                                                                         # （帖子网站地址）
                item['item_type'] = each.find('footer').find('span').find('a').get_text()                                                                                                       # （资源类别，例子：动画）
                item['comment_num'] = each.find('div',{'class':'comments-link',}).find('a').get_text()                                                                                          # （评论数量）
                item['item_time'] = each.find('header').find('div',{'class':'entry-meta',}).find('a').find('time').get_text()                                                                   # （帖子时间）
                item['item_author'] = each.find('header').find('div',{'class':'entry-meta',}).find('span',{'class':'by-author',}).find('span',{'class':'author vcard',}).find('a').get_text()   # （发帖作者）
                item['save_path'] = os.path.join(dataPath,item['item_type'],'第'+now_page_num+'页','['+item['item_time']+']'+item['item_title'])                                                         # （该资源储存的文件夹地址）
            except Exception :
                raise FindError
            else :
                typeDir = os.path.join(dataPath,item['item_type'])
                if not os.path.exists(typeDir):
                    os.makedirs(typeDir)
                pageDir = os.path.join(typeDir,'第'+now_page_num+'页')
                if os.path.exists(pageDir):
                    try:
                        shutil.rmtree(pageDir)
                    except Exception :
                        raise PathError
                os.makedirs(pageDir)
                #提交跟进url
                yield scrapy.Request(url = item['item_url'] , meta = {'item':item} , callback = self.parse_rsc)

    def parse_rsc(self,response):
        '''
        用于解析跟进帖子url后的页面，在此提取资源信息以及返回最终数据
        :param response:响应文件
        :return:GlazedShrineItem
        '''
        shrine = GlazedShrineItem()
        item = response.meta['item']
        rsc = RSCItem()
        img = ImageItem()
        sys = ScrapyItem()
        self.pipeline_use_num += 1

        rsc['rsc_msg_all'] = response.xpath('//div[@class="entry-content"]/p/text()').extract()
        rsc['ratings_num'] = response.xpath('//*[@class="post-ratings"]/strong[2]/text()').extract()[0]  # （评分值）

        rsc_link = response.xpath('//div[@class="entry-content"]/pre/text()').extract()
        if rsc_link != []:
            rsc['rsc_msg_all'].append(rsc_link[0])

        img_all_url = response.xpath('//div[@class="entry-content"]/p/img/@src').extract()
        img['img_item_url'] = img_all_url[0]  # （帖子图片url）
        img_all_url.remove(img_all_url[0])
        img['img_rsc_url'] = ','.join(img_all_url)  # （资源内景图片url，多个图片则用’，‘中文逗号分割组成字符串）
        img['img_path'] = os.path.join(item['save_path'], 'img')  # （图片的保存地址）
        print('img)rsc_url = '+ str(img['img_rsc_url']))

        sys['pipeline_use_num'] = self.pipeline_use_num
        sys['spider_use_time'] = self.spider_start_time
        sys['spider_start_time'] = self.spider_start_time

        shrine['itemItem'] = str(item)# 帖子
        shrine['rscItem'] = str(rsc)# 资源
        shrine['imgItem'] = str(img)# 图片
        shrine['scrapyItem'] = str(sys)# 系统

        yield shrine

#自定义异常父类
class MyException(Exception):
    def __init__(self,*args):
        self.args = args

#输入异常
class InputError(MyException):
    def __init__(self, code=100, message='输入异常！！！', args=('输入异常',)):
        self.args = args
        self.message = message
        self.code = code

#查找异常
class FindError(MyException):
    def __init__(self, code=400, message='查找异常！！！', args=('查找异常',)):
        self.args = args
        self.message = message
        self.code = code

#路径异常
class PathError(MyException):
    def __init__(self, code=400, message='路径异常！！！', args=('路径异常',)):
        self.args = args
        self.message = message
        self.code = code