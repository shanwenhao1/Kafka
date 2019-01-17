#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/11
# @Author  : Wenhao Shan
# @DSC     : Test of admin client model
import sys
import os
import unittest
# 解决命令行运行测试文件找不到文件
cur_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(cur_path)

from domain.model.client_admin_model import ClientAdmin
from infra.utils.error import ActionError


Test_Topic = "test_topic"


class TestClientAdmin(unittest.TestCase):
    """
    测试admin client封装类函数功能
    """
    test_topic = "test_topic"

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def mock_test_topic(topic_name: str, client: ClientAdmin = None):
        """
        模拟创建topic
        :return:
        """
        if client:
            client.create_topic(topic_name)
        else:
            with ClientAdmin() as client:
                client.create_topic(topic_name)

    @staticmethod
    def mock_clear_topic(topic_name: str, client: ClientAdmin = None):
        """
        删除模拟创建的topic
        :return:
        """
        if client:
            client.delete_topic(topic_name)
        else:
            with ClientAdmin() as client:
                client.delete_topic(topic_name)

    def test_create_topic(self):
        """
        测试kafka集群创建topic
        :return:
        """
        with ClientAdmin() as client:
            result = client.create_topic(self.test_topic)
            topic_error_tuples = (result.topic_errors if hasattr(result, 'topic_errors') else result.topic_error_codes)
            for topic, error_code in map(lambda e: e[:2], topic_error_tuples):
                self.assertEqual(error_code, 0), "create test_topic failed, error_code is not equal to 0!"
            # 测试后删除topic
            self.mock_clear_topic(self.test_topic, client)

    def test_delete_topic(self):
        """
        测试kafka集群删除topic
        :return:
        """
        with ClientAdmin() as client:
            # 测试前创建topic
            self.mock_test_topic(self.test_topic, client)
            client.delete_topic(self.test_topic)


class TestClientAdmin2(TestClientAdmin):
    """
    测试clientAdmin类继承(添加测试前和测试后的topic的自动创建和销毁工作)
    """

    def setUp(self):
        self.mock_test_topic(self.test_topic)

    def tearDown(self):
        self.mock_clear_topic(self.test_topic)

    def test_list_consumer_groups(self):
        """
        测试获取消费者groups
        :return:
        """
        with ClientAdmin() as client:
            consumer_group = client.list_consumer_groups()
            print(consumer_group)
