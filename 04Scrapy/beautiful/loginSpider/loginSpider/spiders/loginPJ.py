# -*- coding: utf-8 -*-
import scrapy,logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
#loginUrl = 'https://www.pujinziben.com/front/login.do'

class LoginpjSpider(scrapy.Spider):
    name = 'loginPJ'
    allowed_domains = ['www.pujinziben.com']
    start_urls = ['https://www.pujinziben.com/account.html']

    def start_requests(self):
        for url in self.start_urls :
            yield scrapy.FormRequest(
                url = url,
                cookies = {'cookie':SeleniumLogin()},# 使用selenium登录 ‘普金资本’
                callback = self.parsePage
            )

    def parsePage(self,response):
        print('Login Success !!!')
        print(response.url)

def SeleniumLogin():
    driver = webdriver.Firefox()
    driver.get('https://www.pujinziben.com/login.html')

    if not driver.find_element_by_xpath('//*[@id="username"]').get_attribute('value'):
        driver.find_element_by_id('username').send_keys('13576639986')
    driver.find_element_by_id('password').send_keys('ZT123zlt')
    #js = "alert('请手动滑动滑块，时间限制：5秒内！！！')"

    #driver.execute_script(js)#网站有反js注入！！！
    time.sleep(5)
    print('I am Coming!!!')
    driver.find_element_by_class_name('btn').click()
    # 获取cookies
    print('cookie'+str(driver.get_cookies()))
    return loadCookie(driver.get_cookies())

def loadCookie(cookies):
    cookie_list = []
    for i in cookies:
        print('i[name]='+str(i['name'])+',i[value]='+str(i['value']))
        cookie = i['name'] + '=' + i['value']
        cookie_list.append(cookie)
    cookie_str = ';'.join(cookie_list)  # 获取到Cookie后进行拼接
    return cookie_str