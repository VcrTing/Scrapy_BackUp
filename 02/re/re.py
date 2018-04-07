import re as r
#Here is re

'''
apattern = r.compile(r'\d+')

m = apattern.match('aaaa333bbb456',4,8)
print(m.group())

print('-'*40)

#re.I忽略大小写，re.S全文匹配
apattern = r.compile(r'([a-z]+) ([a-z]+)',re.I)
#两组，只匹配hello world
m = apattern.match('hello world Hello Python')

print(m.group(1))
'''

p = r.compile(r'(\w+) (\w+)')

stri = 'Hello 123,hello 456'

m = p.sub('hello world',stri)

print(m)