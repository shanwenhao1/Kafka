#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/17
# @Author  : Wenhao Shan
import unittest
import json

from domain.model.client_model.producer_model import Producer
from domain.model.client_model.client_admin_model import ClientAdmin
from domain.model.client_model import TIME_OUT
from test.test_client_model.test_client_admin import TestClientAdmin


class TestProducer(unittest.TestCase):
    """
    Test of Producer
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_flush(self):
        """
        测试刷新buffer
        :return:
        """
        with Producer() as producer:
            producer.flush()

    def test_metrics(self):
        """
        获取producer performance
        :return:
        """
        with Producer() as producer:
            performance = producer.metrics()
            print(performance)


class TestProducer2(TestProducer):
    """
    Test for Producer that some function need create something begin, like topic
    """

    def setUp(self):
        self.key = "test_key"
        TestClientAdmin.mock_test_topic(TestClientAdmin.test_topic)

    def tearDown(self):
        TestClientAdmin.mock_clear_topic(TestClientAdmin.test_topic)

    def test_partitions_set_get(self):
        """
        测试获取topic的所有分区
        :return:
        """
        with Producer() as producer:
            par_set = producer.partition_set_get(TestClientAdmin.test_topic)
            print(par_set)
            self.assertEqual(len(par_set), ClientAdmin.Num_Partitions), "Test get partition set failed, set error!!!"

    def test_send(self):
        """
        测试发送数据
        :return:
        """
        test_msg = {
            "test_code": 1,
            "test_info": "test_info"
        }
        message = json.dumps(test_msg)
        msg_byte = message.encode("utf-8")
        with Producer() as producer:
            result = producer.send_message(TestClientAdmin.test_topic, msg_byte, self.key).get(timeout=TIME_OUT)
            print("producer test send data: ", result)
            result_2 = producer.send_message(TestClientAdmin.test_topic, msg_byte, self.key).get(timeout=TIME_OUT)
            print("producer test send data: ", result_2)
            self.assertTrue(result.topic, TestClientAdmin.test_topic), "Test send producer data error, topic error!"
            self.assertEqual(result.topic_partition, result_2.topic_partition), "Test send producer data error, " \
                "same key to different partition"
