from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import PIL.Image
import requests

loginUrl = 'https://accounts.douban.com/login?alias=13576639986&redir=https%3A%2F%2Fwww.douban.com%2F&source=index_nav'
loginAcc = '13576639986'
loginPwd = 'ZT123zlt'

driver = webdriver.PhantomJS()

driver.get(loginUrl)

assert '登录豆瓣' in driver.title

emailValue = driver.find_element_by_xpath('//*[@id="email"]').get_attribute('value')
if not emailValue:
    driver.find_element_by_id('email').send_keys(loginAcc)

driver.find_element_by_id('password').send_keys(loginPwd)

imageUrl = driver.find_element_by_id('captcha_image').get_attribute('src')
image = requests.get(imageUrl).content
with open('captcha.jpg','wb') as f:
    f.write(image)

loginCapt = input('输入验证码（验证图片已保存至本地）：')

driver.find_element_by_id('captcha_field').send_keys(loginCapt)

driver.find_elements_by_name('login')[0].click()

#获取cookie
cookies = driver.get_cookies()
#获取到Cookie后进行拼接，以便后面使用
cookie_list =[]
for i in cookies:
    cookie =i['name']+'='+i['value']
    cookie_list.append(cookie)
cookie_str = ';'.join(cookie_list)
print(cookie_str)

#保存网站快照
driver.save_screenshot('loginDouBan.png')

#正常登录的cookie:
'''
bid=hbOD3VARt64;
__yadk_uid=LhJoprmjpGeIgwX74dAlZKKlrqEi3Yqv;
ll="118215"; ps=y;
_ga=GA1.2.1706336506.1522151416;
_pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1522203663%2C%22https%3A%2F%2Fwww
.baidu.com%2Flink%3Furl%3D1MjS6shF_aKosAq2IGtF2ye-pVY2DbfjRiO1WZ_gZ7mfe45GZkA2jJi8Enu8qThV%26wd%3D%26eqid%3Dd83842400000a8e1000000065abafc0c%22%5D;
__utma=30149280.1706336506.1522151416.1522200115.1522203665.4;
__utmz=30149280.1522203665.4.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic;
_pk_id.100001.8cb4=bce4ad1616d258fc.1522151415.4.1522203694.1522200114.;
push_noty_num=0;
push_doumail_num=0;
__utmv=30149280.17567;
dbcl2="175672728:VXQgbt9+yGw
'''
#使用Selenium+PhantomJS登录获取的cookie为：
'''
push_doumail_num=0;
push_noty_num=0;
_pk_ses.100001.8cb4=*;
_pk_id.100001.8cb4=8a608f442e21d4c2.1522309747.1.1522309747.1522309747.;
_pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1522309747%2C%22https%3A%2F%2Faccounts
.douban.com%2Flogin%3Falias%3D13576639986%26redir%3Dhttps%253A%252F%252Fwww
.douban.com%252F%26source%3Dindex_nav%22%5D;
ck=E2Ae;
dbcl2="175672728:VXQgbt9+yGw";
ps=y;bid=F2tzrMfDcqY
'''
