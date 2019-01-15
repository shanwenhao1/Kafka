#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/11
# @Author  : Wenhao Shan
# @DSC     : Test of admin client model
import sys
import os
# 解决命令行运行测试文件找不到文件
cur_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(cur_path)

from unittest import TestCase
from domain.model.client_admin_model import ClientAdmin


class TestClientAdmin(TestCase):
    """
    测试admin client封装类函数功能
    """
    def setUp(self):
        self.test_topic = "test_topic"

    def tearDown(self):
        pass

    def test_create_topic(self):
        """
        测试kafka集群创建topic
        :return:
        """
        with ClientAdmin() as client:
            client.create_topic(self.test_topic)

    def test_delete_topic(self):
        """
        测试kafka集群删除topic
        :return:
        """
        with ClientAdmin() as client:
            client.delete_topic(self.test_topic)
