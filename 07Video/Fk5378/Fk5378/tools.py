import os
import re
import time
import shutil

"""
    磁盘工具
"""
def dir_maker(target_dir):
    try:
        if os.path.exists(target_dir):
            try:
                shutil.rmtree(target_dir)
            except Exception :
                raise PathError
        os.makedirs(target_dir)
    except Exception:
        raise PathError
    else:
        return True

"""
    Item 提取
"""
# 提取中文
def get_ch(value):
    return re.findall(r'[\u4e00-\u9fa5]+', value)

"""
    Item 删除
"""

def remove_ntr(value):
    return str(value).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '').replace(r'\u3000',' ')

def remove_ntr_re(value, role = '\s'):
    rex = re.compile(role)
    return rex.sub('', str(value))

def remove_item(target_str, trash_item):
    return str(target_str).replace(trash_item, '')

def remove_item_re(target_str, trash_list):
    new_str = ''
    for trash in trash_list:
        rex = re.compile(trash)
        new_str = rex.sub('', target_str)
    print('new_str', new_str)
    return new_str

""" 
    异常处理
"""

#自定义异常父类
class MyException(Exception):
    def __init__(self,*args):
        self.args = args

#输入异常
class InputError(MyException):
    def __init__(self, code=100, message='输入异常！！！', args=('输入异常',)):
        self.args = args
        self.message = message
        self.code = code

#查找异常
class FindError(MyException):
    def __init__(self, code=400, message='查找异常！！！', args=('查找异常',)):
        self.args = args
        self.message = message
        self.code = code

#路径异常
class PathError(MyException):
    def __init__(self, code=400, message='路径异常！！！', args=('路径异常',)):
        self.args = args
        self.message = message