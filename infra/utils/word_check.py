#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/03/01
# @Author  : Wenhao Shan


def pass_word_check(password: str):
    """
    校验密码是否符合规范, 6-16数字+字母
    https://blog.csdn.net/xm_csdn/article/details/77833583?locationNum=9&fps=1
    :param password:
    :return:
    """
    # 校验长度
    if len(password) < 6 or len(password) > 16:
        return False
    # 校验是否全为数字
    if str.isdigit(password):
        return False
    # 校验是否含有数字和字母之外的字符
    if not str.isalnum(password):
        return False
    return True
