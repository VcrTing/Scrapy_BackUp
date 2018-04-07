import urllib.parse
import urllib.request as urllib2
import sys

url = 'http://www.baidu.com/s?'
wd = {'wd':'传智博客'}

#使用urllib.urlencode进行编码转换
print('{wd:传智博}客 的url编码为：')
m = urllib.parse.urlencode(wd)
print(m)
print('-------------------')
print('wd=传智博客 的JBK格式：')
j = urllib.parse.unquote(m)
print(j)

print('例子：')

url = 'https://www.baidu.com'

keyword = input('请输入要查询的字符串：')

wd = {"wd":keyword}
wd = urllib.parse.urlencode(wd)

#仿造的请求头
headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/65.0.3325.181 Safari/537.36'
}
#组合完整的url地址
fullUrl = url+'?'+wd

req = urllib2.Request(fullUrl,headers=headers)
print(type(req))
response = urllib2.urlopen(req)
print('-----=----')
file = open('baiduSearch.text','w')
nr = str(response.read()).replace(r'\r','\r').replace(r'\n','\n').replace(r'\t','\t').replace(r' ','')
file.write(nr)
file.close()