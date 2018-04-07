from pytesseract import *
from PIL import Image

#打开图片
img = Image.open('349371-102.jpg')
print(img)
text = image_to_string(img)
print('result:')
print(text)
print('最后你还是没安装成功哈哈！！！')