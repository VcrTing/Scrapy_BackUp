import urllib.parse
import urllib.request

#Handler是代理设置
#在HTTPHandler里面设置debuglevel=1将会自动打开Debug log模式
#执行的时候会自动打印收发包
http_handler = urllib.request.HTTPHandler(debuglevel=1)
#构造Opener
opener = urllib.request.build_opener(http_handler)

#
Headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
}
request = urllib.request.Request('http://www.baidu.com/',headers=Headers)

response = opener.open(request)

with open('HAO.txt','w') as f:
    f.write(str(response.read()).replace(r'\r','\r').replace(r'\n','\n').replace(r'\t','\t'))

print(response.read())