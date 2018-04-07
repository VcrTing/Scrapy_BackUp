from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#创建webdriver
driver = webdriver.PhantomJS()

#加载网页
driver.get('http://www.baidu.com')

#向id=kw的控件输入'美女'
driver.find_element_by_id('kw').send_keys(u'美女')

#保存网站快照
driver.save_screenshot('baidu.png')

#之后点击一个链接
#driver.find_element_by_id('').click()