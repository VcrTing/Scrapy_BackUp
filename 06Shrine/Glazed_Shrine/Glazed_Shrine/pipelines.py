# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import codecs,os,datetime,requests,json,re,time

BASE_DIR = os.path.dirname(__file__)

class GlazedShrinePipeline(object):
    def process_item(self, item, spider):
        return item

class PathShrinePipeline(object):
    def __init__(self):
        self.file = None

    def process_item(self, item, spider):
        itemItem = eval(item['itemItem'])                 # 帖子
        rscItem = eval(item['rscItem'])                   # 资源
        imgItem = eval(item['imgItem'])                   # 图片
        sysItem = eval(item['scrapyItem'])                # 系统

        print('img_path = '+ str(os.path.join(imgItem['img_path'],str(itemItem['item_title']+imgItem['img_item_url'][-6:]).replace(r'/','_'))))
        if not os.path.exists(itemItem['save_path']):
            os.makedirs(itemItem['save_path'])
        if not os.path.exists(imgItem['img_path']):
            os.makedirs(imgItem['img_path'])
        '''
        addr = []
        down = []
        for ii in rscItem['rsc_msg_all']:
            p = re.compile(r'\w{30,}')
            down_addr = re.findall(p , ii)
            addr.append(down_addr)
        addr = [x for x in addr if x != []]
        for ii in addr:
            down.append(ii[0])
        rscItem['down_addr'] = ','.join(down)'''
        #写入数据
        DATA_SAVE = {
            "\nitem_title":itemItem['item_title'],
            "\nitem_content":itemItem['item_content'],
            "\nitem_url":itemItem['item_url'],
            "\nitem_type":itemItem['item_type'],
            "\ncomment_num":itemItem['comment_num'],
            "\nitem_time":itemItem['item_time'],
            "\nitem_author":itemItem['item_author'],
            "\nrsc_msg_all":rscItem['rsc_msg_all'],
            "\nratings_num":rscItem['ratings_num'],
            "\nimg_path":imgItem['img_path'],
            "\npipeline_use_num":sysItem['pipeline_use_num'],
            "\nget_time":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
        }
        self.file = codecs.open(os.path.join(itemItem['save_path'],'DATA_SAVE.txt'), 'wb', encoding='utf-8')
        self.file.write(str(DATA_SAVE).replace(r'\n','\n\n').replace(r'\u3000',' '))

        #写入图片
        image = requests.get(imgItem['img_item_url']).content
        item_img_path = os.path.join(imgItem['img_path'],str(itemItem['item_title']+imgItem['img_item_url'][-6:]).replace(r'/','_'))
        with open(item_img_path, 'wb') as f:
            f.write(image)

        if imgItem['img_rsc_url'] :
            img_rsc_url = imgItem['img_rsc_url'].split(',')
            for i,iru in enumerate(img_rsc_url,1) :
                image = requests.get(iru).content
                item_img_path = os.path.join(imgItem['img_path'], str(i)+ '张' + imgItem['img_item_url'][-6:])
                with open(item_img_path, 'wb') as f:
                    f.write(image)

        print('-'*80)

    def close_spider(self, spider):
        self.file.close()

class MysqlShrinePipeline(object):

    def __init__(self):
        # 打开数据库连接
        self.conn = pymysql.connect('localhost','root','ZT123zlt','shrine',charset="utf8")
        self.cursor = self.conn.cursor()
        # 创表与清空表
        self.cursor.execute(createTableShrine)
        self.conn.commit()
        self.cursor.execute('truncate table Shrine;')
        self.conn.commit()

    def process_item(self, item, spider):
        print('mysql------------------------------>')
        itemItem = eval(item['itemItem'])                 # 帖子
        rscItem = eval(item['rscItem'])                   # 资源
        imgItem = eval(item['imgItem'])                   # 图片
        sysItem = eval(item['scrapyItem'])                # 系统
        #清洗数据
        addr = []
        down = []
        for ii in rscItem['rsc_msg_all']:
            p = re.compile(r'\w{30,}')
            down_addr = re.findall(p, ii)
            addr.append(down_addr)
        addr = [x for x in addr if x != []]
        for ii in addr:
            down.append(ii[0])
        rscItem['down_addr'] = ','.join(down)
        #凑齐数据
        item_title = itemItem['item_title']#（帖子标题）
        item_content = itemItem['item_content']#（帖子内容）
        item_url = itemItem['item_url']#（帖子网站地址）
        item_time = itemItem['item_time']#（帖子时间）
        save_addr = itemItem['save_path']#（该资源储存的文件夹地址）
        img_item_path = str(os.path.join(imgItem['img_path'],str(itemItem['item_title']+imgItem['img_item_url'][-6:]).replace(r'/','_')))#（帖子图片路径）
        item_type = itemItem['item_type']#（资源类别）
        down_addr = rscItem['down_addr']#（下载地址）
        ratings_num = rscItem['ratings_num']#（评分）
        comment_num = itemItem['comment_num']#（帖子评论数量）

        #执行SQL插入数据
        self.cursor.execute(insertShrine,(item_title,item_content,item_url,item_time,save_addr,img_item_path,item_type,down_addr,ratings_num,comment_num))
        self.conn.commit()
        print('mysql------------------------------<')
        return item

    def close_spider(self, spider):
        self.conn.close()
# 创建 Shrine 表
createTableShrine = \
            "CREATE TABLE IF NOT EXISTS Shrine(" \
                "Id INT PRIMARY KEY AUTO_INCREMENT," \
                "item_title VARCHAR(300) ," \
                "item_content VARCHAR(300) ," \
                "item_url VARCHAR(100) ," \
                "item_time VARCHAR(100) ," \
                "save_addr VARCHAR(300) ," \
                "img_item_path VARCHAR(300) ," \
                "item_type VARCHAR(30) ," \
                "down_addr VARCHAR(300) ," \
                "ratings_num VARCHAR(30) ," \
                "comment_num VARCHAR(30) " \
            ")"
insertShrine = \
            "INSERT INTO Shrine(" \
            "item_title,item_content,item_url,item_time," \
            "save_addr,img_item_path,item_type,down_addr," \
            "ratings_num,comment_num) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
