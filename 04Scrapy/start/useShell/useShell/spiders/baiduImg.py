# -*- coding: utf-8 -*-
import scrapy


class BaiduimgSpider(scrapy.Spider):
    name = 'baiduImg'
    allowed_domains = ['image.baidu.com']
    start_urls = ['https://image.baidu.com/']

    def parse(self, response):
        a,b,s = 0,1,0
        n = 5
        while s < n :
            a,b = b,a+b
            s = s+1
            print(b)
        print('-'*30)


        a = again(n)
        for i in a:
            print(i)

def again(n):
    a, b, s = 0, 1, 0
    n = 5
    while s < n:
        a, b = b, a + b
        s = s + 1
        yield b