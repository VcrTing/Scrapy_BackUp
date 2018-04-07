import json
import jsonpath

#读取出json_file,你也可以用requests读取网站上的json：www.lagou.com/lbs/getAllCitySearchLabels.json
json_file = open('chinaCity.json','r').read()

print(type(json_file))

#使用jsonPath
city_list = jsonpath.jsonpath(json_file,'$..name')

print(city_list)