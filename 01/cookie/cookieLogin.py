import urllib.parse
import urllib.request
import http.cookiejar

#Cookie jar
cookie = http.cookiejar.CookieJar()

#通过处理器类构建一个处理器对象，
#参数就是构建的CookieJar对象
cookie_handler = urllib.request.HTTPCookieProcessor(cookie)

#构建一个自定义的opener
opener = urllib.request.build_opener(cookie_handler)

#自定义opener的addheaders的参数，可以赋值HTTP报头参数
opener.addheaders = [
    ('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linu…) Gecko/20100101 Firefox/59.0')
]#list、 tuple type

#登录的url
loginUrl = 'https://gitee.com/login'

#webPage's css'name
data = {
    'user[login]':'13576639986',
    'user[password]':'ZT123zlt',
}

#通过urlencode()编码转换
datas = urllib.parse.urlencode(data).encode(encoding='utf-8')
print(datas)

request = urllib.request.Request(loginUrl,data=datas)#no headers,already add

print(request)
#发送第一次post请求，生成登录后的cookie,一并发到服务器
response = opener.open(request)


print(response.getcode())

#目标url
getUrl = 'https://gitee.com/profile'

#获取登录后才能访问的页面
addrResponse = opener.open(getUrl)

with open('cookieLogin.txt','w') as f:
    f.write(str(addrResponse.read()))