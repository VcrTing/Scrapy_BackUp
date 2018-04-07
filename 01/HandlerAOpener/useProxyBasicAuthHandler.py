
import urllib.request

test = 'test'

password = '123456'

webserver = '192.168.21.52'

#构建一个密码管理器
passwordMgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

#添加授权信息，第一个参数没有说就写None
passwordMgr.add_password(None,webserver,test,password)

httpauth_handler = urllib.request.HTTPBasicAuthHandler(passwordMgr)

opener = urllib.request.build_opener(httpauth_handler)

req = urllib.request.Request('https://'+webserver)
response = urllib.request.urlopen(req)

print(response.read())