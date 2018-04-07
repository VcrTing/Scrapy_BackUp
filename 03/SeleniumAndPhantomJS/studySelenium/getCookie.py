from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

#得到FireFox
driver = webdriver.Firefox()

#getUrl
driver.get('https://www.bilibili.com/')

#存入cookie :>
cookie = {
    'name':'foo','value':'bar'
}
driver.add_cookie(cookie_dict=cookie)

#提得cookie
driver.get_cookie(cookie)