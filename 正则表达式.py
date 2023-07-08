# -*-coding = utf-8 -*-
# @Time : 2023/7/7 20:22
# @Author : 万锦
# @File : 正则表达式.py
# @Softwore : PyCharm

import re

def email_re(str_re):
    obj = re.compile("^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")
    return re.match(obj,str_re)

def tel_re(str_re):
    obj = re.compile("^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$")
    return re.match(obj, str_re)

if __name__ == '__main__':

    test_str = "56461561615@gamil.com"
    if email_re(test_str):
        print(1)
