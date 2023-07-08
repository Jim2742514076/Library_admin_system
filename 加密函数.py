# -*-coding = utf-8 -*-
# @Time : 2023/7/7 16:56
# @Author : 万锦
# @File : 加密函数.py
# @Softwore : PyCharm

import hashlib

def md5(str):
    hash = hashlib.md5(bytes("图书管理系统，欧耶",encoding="utf-8"))
    hash.update(bytes(str,encoding='utf-8'))
    return hash.hexdigest()



