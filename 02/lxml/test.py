import requests
import os

url = 'https://imgsa.baidu.com/forum/w%3D580/sign=bbe3c565b0315c6043956be7bdb1cbe6/6ce61f4c510fd9f98c373c19292dd42a2834a4b8.jpg'
html = requests.get(url)
with open('picture.jpg', 'wb') as file:
    file.write(html.content)