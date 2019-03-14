#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/03/04
# @Author  : Wenhao Shan

import hashlib


def generate_md5(text: str):
    """
    generate md5
    :param text: str that you want to generate md5
    :return:
    """
    str_md5 = hashlib.md5()
    str_md5.update(text.encode("utf-8"))
    return str_md5.hexdigest()
