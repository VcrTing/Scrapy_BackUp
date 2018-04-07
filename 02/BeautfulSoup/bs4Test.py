from bs4 import BeautifulSoup
import requests
import os

sess = requests.Session()  #构建一个session对象

def captcha(captcha_url):
    #处理豆瓣登录时的验证码图片
    cimg = sess.get(captcha_url).content
    with open('captcha.jpg','wb') as f:
        f.write(cimg)
    print('验证码图片已保存到当前目录～')
    cap_value = input('请输入图片验证码：')
    return cap_value

def MYLogin():

    Headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    html = sess.get('https://accounts.douban.com/login?alias=&redir=https%3A%2F%2Fwww.douban.com%2F&source=index_nav',headers = Headers).text#会记录网页的cookie值
    print(html)
    bs = BeautifulSoup(html,'html.parser')#调用lxml解析库
    login_url = bs.find(attrs={'id': 'lzform'})['action']

    data = {
        'ck':bs.find(attrs={'name': 'ck'})['value'],
        'source':bs.find(attrs={'name':'source'})['value'],
        'redir':bs.find(attrs={'name':'redir'})['value'],
        'form_emil':input('请输入你的豆瓣手机号/邮箱/用户名：'),
        'form_password':input('请输入你的豆瓣登录密码：'),
        'captcha-solution':captcha(bs.find(attrs={'id':'captcha_image'})['src']),#调用处理验证码图片方法
        'captcha-id':bs.find(attrs={'name':'captcha-id'})['value'],
        'logion':'登录'
    }
    input('准备登录:'+str(login_url)+'，请检查一下你的Form表单：\n'+str(data))

    html = sess.post(login_url,data=data,headers=Headers)
    print(html.url)

MYLogin()
print('You  cant login DouBan!!! now')