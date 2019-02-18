#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/17
# @Author  : Wenhao Shan
# @DSC     : Test of simple_client model

import sys
import os
import unittest
# 解决命令行运行测试文件找不到文件
cur_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(cur_path)


class ClientTest(unittest.TestCase):
    """
    Test of Client
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass
