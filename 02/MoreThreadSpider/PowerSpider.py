import threading#线程
from queue import Queue#队列
from lxml import etree#解析
import requests#请求
import json#储存

#循环退出条件
CRAWL_EXIT = True
#解析退出条件
PARSE_EXIT = True

class ThreadParse(threading.Thread):
    def __init__(self,threadName,dataQueue,fileName):
        super(ThreadParse,self).__init__()
        self.threadName = threadName
        self.dataQueue = dataQueue
        self.fileName = fileName

    def run(self):
        print('启动'+self.threadName+'-->')
        while not PARSE_EXIT:
            try:
                html = self.dataQueue.get(False)
                self.parse(html)
            except:
                print('dataQueue is Empty!!!')
        print('<--'+self.threadName+'结束')

    def parse(self,html):
        theHtml = etree.HTML(html)
        nodeList = theHtml.xpath('//div[@class="article block untagged"]')
        for node in nodeList:
            userName = node.xpath('div[@class="author"]/a[2]/h2/text')
            userUrl = node.xpath('div[@class="author"]/a[1]/@href')
            nodeText = node.xpath('a[@class="contentHerf"]/div/span/text')
            textUrl = node.xpath('a[@class="contentHerf"]/@href')
            rating = node.xpath('div[@class="stats"]/span[@class="stats-vote"]/i/text')
            item = {#封装数据
                'userName':userName,
                'userUrl':userUrl,
                'nodeText':nodeText,
                'textUrl':textUrl,
                'rating':rating
            }
            json_data = json.dump(item,ensure_ascii=False)#转json格式
            with open(self.fileName,'wb') as f:
                f.write(json_data)

class ThreadCrawl(threading.Thread):
    def __init__(self,threadName,pageQueue,dataQueue):
        #threading.Thread.__init__(self)
        super(ThreadCrawl,self).__init__()
        self.threadName = threadName
        self.pageQueue = pageQueue
        self.dataQueue = dataQueue
        self.headers = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }

    def run(self):
        print('启动'+self.threadName+'-->')
        while not CRAWL_EXIT:
            try:
                #可选参数block,默认值为True，如果队列为空，block为True，就会进入阻塞状态
                #如果队列为空，block为False的话，就弹出一个Queue.empty()异常
                page = self.pageQueue.get()#取出一个，先进的先出
                url = 'https://www.qiushibaike.com/8hr/page/'+str(page)+'/'
                content = requests.get(url,headers = self.headers)
                self.dataQueue.put(content)
            except:
                print('block=False,throw a empty ERROR!!!')
        print('<--'+self.threadName+'结束')

def main():
    pageQueue = Queue(10)#不写就是无限个页面
    for i in range(1,11):
        pageQueue.put(i)
    #采集结果的队列（每一页的html源码）
    dataQueue = Queue()

    fileName = open('duanzi.json','wb')

    crawlList = ['get01','get02','get03']#三个线程名字
    threadCrawl = []#用来存储线程
    for threadName in crawlList:
        thread = ThreadCrawl(threadName,pageQueue,dataQueue)
        thread.start()
        threadCrawl.append(thread)

    parseList = ['parse01','parse02','parse03']
    threadParse = []
    for threadName in parseList:
        thread = ThreadParse(threadName,dataQueue,fileName)
        thread.start()
        threadParse.append(thread)

    #等待之前的操作执行完毕，采集线程退出循环
    while pageQueue.empty():
        pass

    global CRAWL_EXIT
    CRAWL_EXIT = True
    print('The PageQueue is Empty!!!')

    for thread in threadCrawl:
        thread.join()
        print('-0-')

    for thread in threadParse:
        thread.join()
        print('-1-')

if __name__ == '__main__':
    print('由于技术原因，多线程爬虫未完成，待今回来后完成！！！')