import urllib.request as req

#仿造的请求头
headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/65.0.3325.181 Safari/537.36'
}

#通过Request构造请求对象
request = req.Request('https://www.baidu.com/',headers=headers)#,data={},headers={})

#发送请求，返回类文件对象！！！
response = req.urlopen(request)

#类文件对象支持python文件对象操作方法
#read()读取内容，返回字符串！！！
html = response.read()

# 打印
#print(html)
print('Http的响应码(int)：'+str(response.getcode()))
print('返回实际数据的实际URL，防止重定向问题：'+response.geturl())
print('服务器返回到的报头信息：'+str(response.info()))

#完整headers
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;"
              "q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "BAIDUID=6EA303A3D8ADF8EA008E36EB216CAC17:FG=1; "
              "PSTM=1521707111; BIDUPSID=D338D55F7109501A82C92F3DA6E35223; "
              "BD_UPN=123353; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; "
              "BD_HOME=0; BD_CK_SAM=1; PSINO=7; "
              "BDRCVFR[QxxZVyx49rf]=I67x6TjHwwYf0; "
              "H_PS_645EC=69c6T05u9lycw2o0z0T8vuyxLFFyJvDXlnqENdCTEsNy%2Fzw4TWftXulm0vmPAL7%2BgHQNW5XMfjD16A; "
              "H_PS_PSSID=1468_21127_18559_22158",
    "Host": "www.baidu.com",
    "Upgrade-Insecure-Requests": 1,
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
}