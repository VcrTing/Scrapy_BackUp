from selenium import webdriver
from selenium.webdriver.common.keys import Keys
'''
from pyvirtualdisplay import Display
#连接google chrome需要的代码
display = Display(visible=0, size=(800, 800))
display.start()'''

#加载Chrome实例
driver = webdriver.PhantomJS()
#连接url
driver.get('http://www.baidu.com')
#断言web.title是否含有Python关键
assert '百度' in driver.title

#查找id = kw的元素，给元素发送‘美女’Text
elem = driver.find_element_by_id('kw').send_keys('美女',Keys.ENTER)

#保存网站快照
driver.save_screenshot('baidu.png')

print(elem)
