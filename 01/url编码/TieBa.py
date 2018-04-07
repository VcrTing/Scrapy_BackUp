import urllib.parse
import urllib.request
import os

#pn = '页数-50'
headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
}

def loadPage(url,fileName):
    """
    作用：根据url发送请求，获取服务器响应文件
    :param：
        url：需要爬取的url地址
        fileName：处理后的文件名
    :return:
        response
    """
    print('正在下载：'+fileName)
    request = urllib.request.Request(url,headers=headers)
    return urllib.request.urlopen(request)

def writePage(html,fileName):
    """
    作用：将html内容写入到本地
    :param
        html: 服务器响应的文件内容
        fileName：处理后的文件名
    :return:
        None
    """
    print('正在保存：'+fileName)
    with open(os.path.join('TieBa',fileName),'w') as f:
        f.write(str(html.read()).replace(r'\r','\r').replace(r'\n','\n').replace(r'\t','\t'))
    print('-'*40+'tag'+'-'*40)

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
        fileName = '吧名:'+baName+' 的第'+str(page)+'页.html'
        fullUrl = url + "&pn=" + str(pn)
        html = loadPage(url,fileName)
        print(html.getcode())
        writePage(html,fileName)
    print('谢谢使用！！！')

if __name__ == "__main__":
    kw = input('请输入要爬取的贴吧名：')
    beginPage = int(input('请输入启始页：'))
    endPage = int(input('请输入终止页：'))

    url = 'https://tieba.baidu.com/f?'
    key = urllib.parse.urlencode({"kw":kw})
    url = url + key

    tiebaSpider(url,beginPage,endPage,kw)
