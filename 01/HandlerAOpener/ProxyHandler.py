import urllib.request
import urllib.parse

#代理开关
proxySwith = True

#代理IP是字典类型
proxy_ip = {
    'http':'119.28.152.208/80',
}

#构造有代理的Handler处理器对象
httpProxyHandler = urllib.request.ProxyHandler(proxy_ip)

#构造一个没有代理的Handler处理器对象
nullProxyHandler = urllib.request.ProxyHandler({})

#开始发送请求->
if proxySwith:
    opener = urllib.request.build_opener(httpProxyHandler)
else:
    opener = urllib.request.build_opener(nullProxyHandler)

#构建一个全局的Opener,之后所有的请求都可以用urlopen()方式去发送，也附带Handler的功能
urllib.request.install_opener(opener)

#构造Header
Headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
}

request = urllib.request.Request('https://www.baidu.com/',headers=Headers)
response = urllib.request.urlopen(request)

print(response.getcode())

with open('ProxyHandler.html','w') as f:
    f.write(str(response.read()).replace(r'\r','\r').replace(r'\t','\t').replace(r'\n','\n'))

