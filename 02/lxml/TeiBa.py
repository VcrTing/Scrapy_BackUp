import urllib.parse
import urllib.request
import os
from lxml import etree
import requests
from io import BytesIO
import sys, os

#确定本地文件编码格式
type = sys.getfilesystemencoding()

#获取Session
session = requests.Session()

#pn = '页数-50'
headers = {
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linu…) Gecko/20100101 Firefox/59.0',
}

#帖子链接Xpath

tieXpath = '//*[@id="thread_list"]/li/div/div[2]/div[1]/div[1]/a/@href'
#帖子里的每个图片的Xpath
imgXpath = '//*[@class="BDE_Image"]/@src'

def loadPage(url,fileName):
    """
    作用：根据url发送请求，获取服务器响应文件
    :param：
        url：需要爬取的url地址
        fileName：处理后的文件名
    :return:
        response
    """
    pg = session.get(url)
    print(pg)
    pg.encoding='utf-8'
    html = pg.content
    #解析html文档为HTML DOM模型
    content = etree.HTML(html)
    #返回匹配成功的列表集合
    link_list = content.xpath(tieXpath)
    print(str(link_list))
    for link in link_list:
        fullLink = 'https://tieba.baidu.com'+link
        print(fullLink)
        loadImage(fullLink,fileName)

def loadImage(link,fileName):
    """
    作用：取出每个网页的图片链接
    :param
        link:链接
    :return:
    """
    pg = session.get(link)
    pg.encoding='utf-8'
    html = pg.content
    content = etree.HTML(html)
    link_list = content.xpath(imgXpath,stream=True)
    for link in link_list:
        writeImage(link,fileName)

def writeImage(link,fileName):
    """
    作用：将html内容写入到本地
    :param
        html: 服务器响应的文件内容
        fileName：处理后的文件名
    :return:
        None
    """
    html = requests.get(link)
    fileName = link[-16:]
    with open(os.path.join('TieBa',fileName), 'wb') as file:
        file.write(html.content)

def tiebaSpider(url,beginPage,endPage,baName):
    """
    作用：贴吧爬虫调度器，负责组合处理每个页面的url
    :param:
        url：贴吧url的前部分
        beginPage：起始页
        endPage：结束页
        baName：要爬取的贴吧名
    :return:
        None
    """
    for page in range(beginPage,endPage+1):
        pn = (page - 1)*50#计算
        fileName = baName+' 的'
        fullUrl = url + "&pn=" + str(pn)
        input(fullUrl)
        loadPage(url,fileName)
    print('谢谢使用！！！')

if __name__ == "__main__":
    kw = input('请输入要爬取的贴吧名：')
    beginPage = int(input('请输入启始页：'))
    endPage = int(input('请输入终止页：'))

    url = 'https://tieba.baidu.com/f?kw='+kw#urllib.parse.urlencode({"kw":kw}).encode(encoding='utf-8')
    tiebaSpider(url,beginPage,endPage,kw)
