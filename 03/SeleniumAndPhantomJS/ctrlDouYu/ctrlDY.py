from selenium import webdriver
import unittest#测试模块
from bs4 import BeautifulSoup as bs
import json
import pytesser

class DouYu(unittest.TestCase):
    dataDict = {}

    def setUp(self):
        self.driver = webdriver.PhantomJS()

    def testDouyu(self):
        self.driver.get('https://www.douyu.com/directory/all')
        i = 0
        while True:
            i = i + 1
            iList = []
            soup = bs(self.driver.page_source,'lxml')
            names = soup.find_all('h3',{'class':'ellipsis'})
            seeNums = soup.find_all('span',{'class':'dy-num fr'})
            #把列表合并为元祖
            for name,seeNum in zip(names,seeNums):
                iList.append({'房间名':name.get_text().strip(),'观众人数':seeNum.get_text().strip()})
            DouYu.dataDict['第'+str(i)+'页'] = iList
            if self.driver.page_source.find('shark-pager-disable-next') != -1:
                break
            self.driver.find_element_by_class_name('shark-pager-next').click()

    def tearDown(self):
        with open('DouYu.txt', 'w') as f:
            for chunk in str(DouYu.dataDict):
                f.write(chunk)
        print('-0-')
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()