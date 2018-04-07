import urllib.parse
import urllib.request

#Url
#url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc'
#Header
Headers = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept-Language':'zh-CN,zh;q=0.9',
}

#Key
key = input('请输入要查询的翻译的文字:')

#Post表单数据
postFormData = {
    "i":key,
    "from":"AUTO",
    "to":"AUTO",
    "smartresult":"dict",
    "client":"fanyideskweb",
    "salt":"1522049033562",
    "sign":"92ffb87b997b1a53277e2fe6c39c9055",
    "doctype":"json",
    "version":"2.1",
    "keyfrom":"fanyi.web",
    "action":"FY_BY_REALTIME",
    "typoResult":"false",
}#代替的表单数据
data = {
        "type" : "AUTO",
        "i" : key,
        "doctype" : "json",
        "xmlVersion" : "1.8",
        "keyfrom" : "fanyi.web",
        "ue" : "UTF-8",
        "action" : "FY_BY_CLICKBUTTON",
        "typoResult" : "true"
    }
#
data = urllib.parse.urlencode(data).encode(encoding='utf-8')

request = urllib.request.Request(url,data=data,headers=Headers)

response = urllib.request.urlopen(request)

result = str(response.read()).replace(r'\r','r').replace(r'\n','\n').replace(r'\t','\t')
r = urllib.parse.unquote(result).encode(encoding='utf-8')

with open('youdao.txt','w') as f:
    f.write(str(r))
print('结束！！！')



