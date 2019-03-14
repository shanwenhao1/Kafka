#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/17
# @Author  : Wenhao Shan

import json
import unittest
from domain.model.client_model.consumer_model import Consumer
from domain.model.client_model.producer_model import Producer
from test.test_client_model.test_client_admin import TestClientAdmin
from infra.utils.time_utils import get_now_time_timestamp


class TestConsumer(unittest.TestCase):
    """
    Test of Consumer
    """
    Test_Group_Id = "Test_group_id"

    def setUp(self):
        TestClientAdmin.mock_test_topic(TestClientAdmin.test_topic)

    def tearDown(self):
        TestClientAdmin.mock_clear_topic(TestClientAdmin.test_topic)

    def test_assign(self):
        """
        测试手动分配consumer topic分区
        :return:
        """
        partitions = [(TestClientAdmin.test_topic, 0)]
        with Consumer() as consumer:
            consumer.assign(partitions)

    def test_assignment(self):
        """
        测试获取consumer 当前topic分区
        :return:
        """
        with Consumer() as consumer:
            # 模拟手动创建topic partitions
            partitions = [(TestClientAdmin.test_topic, 0)]
            consumer.assign(partitions)
            # 测试获取topic partitions
            all_partition = consumer.assignment()
            result = all_partition.pop()
            self.assertTrue(result.topic == TestClientAdmin.test_topic), "Test get consumer topic " \
                                                                         "partition failed, topic error"
            self.assertTrue(result.partition == 0), "Test get consumer topic partition failed, offset type error"

    def test_beginning_offsets(self):
        """
        测试获取指定partitions的最开始offset
        :return:
        """
        with Consumer() as consumer:
            # 模拟手动分配topic partitions
            partitions = [(TestClientAdmin.test_topic, 0)]
            consumer.assign(partitions)
            # 测试获取指定partitions的最开始offset
            result = consumer.beginning_offsets(partitions)
            for key, value in result.items():
                self.assertTrue(key.topic == TestClientAdmin.test_topic), "Test get beginning offset failed, " \
                                                                          "topic error"
                self.assertTrue(value == 0), "Test get beginning offset failed, offset type error"

    def test_end_offsets(self):
        """
        测试获取指定partitions的最后一个offset
        :return:
        """
        with Consumer() as consumer:
            # 模拟手动分配topic partitions
            partitions = [(TestClientAdmin.test_topic, 0)]
            # 测试获取指定partitions的最开始offset
            result = consumer.end_offsets(partitions)
            for key, value in result.items():
                self.assertTrue(key.topic == TestClientAdmin.test_topic), "Test get end offset failed, " \
                                                                          "topic error"
                self.assertTrue(value == 0), "Test get end offset failed, offset type error"

    def test_offsets_for_time(self):
        """
        测试根据根据timestamp查询topic partition最早offset
        :return:
        """
        # 模拟手动创建topic partitions
        partitions = [(TestClientAdmin.test_topic, 0), (TestClientAdmin.test_topic, 1), (TestClientAdmin.test_topic, 2)]
        timestamp = get_now_time_timestamp()
        with Consumer(self.Test_Group_Id) as consumer:
            result = consumer.offsets_for_time(partitions, timestamp)
            for key, value in result.items():
                self.assertTrue(key.topic == TestClientAdmin.test_topic), "Test get offset by time failed, topic error"
                self.assertTrue(value is None), "Test get offset by time failed, offset error"

    def test_highwater(self):
        """
        测试查询highwater offset
        :return:
        """
        with Consumer(self.Test_Group_Id) as consumer:
            # 模拟手动分配topic partitions
            partitions = [(TestClientAdmin.test_topic, 0)]
            consumer.assign(partitions)
            result = consumer.highwarter(TestClientAdmin.test_topic, 0)
            self.assertTrue(result is None), "Test get highwater offset failed, offset error"

    def test_commit(self):
        """
        测试commit offset
        :return:
        """
        offset = (TestClientAdmin.test_topic, 0, 7)
        with Consumer(self.Test_Group_Id) as consumer:
            # 测试普通commit
            consumer.commit(offset)
            # 测试async commit
            consumer.commit(offset, async_commit=True)

    def test_committed(self):
        """
        测试查询指定的topic partition最后一个committed offset
        :return:
        """
        offset = (TestClientAdmin.test_topic, 0, 7)
        with Consumer(self.Test_Group_Id) as consumer:
            # mock commit offset
            consumer.commit(offset)
            result = consumer.committed(TestClientAdmin.test_topic, 0)
            self.assertEqual(result, 7), "Test get last committed offset of topic partition failed, offset error"

    def test_metrics(self):
        """
        测试获取获取consumer的性能记录
        :return:
        """
        with Consumer() as consumer:
            performance = consumer.metrics()
            print(performance)

    def test_partition_for_topic(self):
        """
        测试查询指定topic的分区metadata
        :return:
        """
        with Consumer(self.Test_Group_Id) as consumer:
            # 模拟生成topic的单个分区的metadata
            # offset = (TestClientAdmin.test_topic, 0, 7)
            # consumer.commit(offset)
            result = consumer.partition_for_topic(TestClientAdmin.test_topic)
            print(result)
            self.assertTrue(len(result) > 0 and type(result) == set), "Test get partition of topic failed, return error"

    def test_pause(self):
        """
        测试挂起分区请求
        :return:
        """
        topic_partition = [(TestClientAdmin.test_topic, 0), (TestClientAdmin.test_topic, 1),
                           (TestClientAdmin.test_topic, 2)]
        with Consumer() as consumer:
            # 模拟手动分配topic partitions
            consumer.assign(topic_partition)
            # 测试pause挂起功能
            consumer.pause(topic_partition)

            # 测试获取挂起分区信息
            result = consumer.get_paused()
            self.assertEqual(len(result), len(topic_partition)), "Test pause and get pause error, " \
                                                                 "missing topic partition data"
            _topic_partition = [(_par.topic, _par.partition) for _par in result]
            for _partition in _topic_partition:
                self.assertTrue(_partition in topic_partition), "Test pause and get pause error, " \
                    "result is not equal to request"

    def test_resume(self):
        """
        测试resume恢复
        :return:
        """
        topic_partition = [(TestClientAdmin.test_topic, 0), (TestClientAdmin.test_topic, 1),
                           (TestClientAdmin.test_topic, 2)]
        with Consumer() as consumer:
            # 模拟挂起
            consumer.assign(topic_partition)
            consumer.pause(topic_partition)
            result = consumer.get_paused()
            self.assertEqual(len(result), len(topic_partition)), "Test resume failed, mock pause data failed"
            # 测试resume
            consumer.resume(topic_partition)
            result = consumer.get_paused()
            self.assertEqual(len(result), 0), "Test resume failed, resume not succeed"

    def test_seek(self):
        """
        测试手动修改offset
        :return:
        """
        with Consumer() as consumer:
            # 模拟手动分配topic partition
            partitions = [(TestClientAdmin.test_topic, 0)]
            consumer.assign(partitions)
            consumer.seek(partitions[0], 1)
            result = consumer.position(partitions[0])
            self.assertEqual(result, 1), "Test seek failed, seek offset is not 1"

    def test_seek_many(self):
        """
        测试批量seek
        :return:
        """
        topic_partition = [(TestClientAdmin.test_topic, 0), (TestClientAdmin.test_topic, 1),
                           (TestClientAdmin.test_topic, 2)]
        with Consumer() as consumer:
            # 模拟手动分配topic partition
            consumer.assign(topic_partition)
            consumer.seek_many()
            result = consumer.position(topic_partition[0])
            self.assertEqual(result, 0), "Test seek to the beginning failed, seek offset is not 0"
            consumer.seek_many(topic_partition, is_begin=False)
            result = consumer.position(topic_partition[0])
            print(result)
            self.assertEqual(result, 0), "Test seek to the end failed, seek offset is not 0"

    def test_poll(self):
        """
        测试批量获取records
        :return:
        """
        test_data = {
            "test_msg": "test",
            "time_test": 1000,
        }
        test_data_str = json.dumps(test_data)
        with Consumer() as consumer:
            # 模拟手动分配topic partition
            partitions = [(TestClientAdmin.test_topic, 0), (TestClientAdmin.test_topic, 1),
                          (TestClientAdmin.test_topic, 2)]
            consumer.assign(partitions)
            with Producer() as producer:
                producer.send_message(TestClientAdmin.test_topic, test_data_str.encode("utf-8"), "test_key")
                producer.send_message(TestClientAdmin.test_topic, test_data_str.encode("utf-8"), "test_key")
            consumer.seek_many(partitions)
            self.assertEqual(consumer.position(partitions[0]), 0), "Test poll failed, seek many to begin failed"
            self.assertEqual(consumer.position(partitions[1]), 0), "Test poll failed, seek many to begin failed"
            self.assertEqual(consumer.position(partitions[2]), 0), "Test poll failed, seek many to begin failed"
            result = consumer.poll(100)
            self.assertEqual(len(result[list(result.keys())[0]]), 2), "Test poll failed, missing data"
            for key, value in result.items():
                self.assertEqual(value[0].topic, TestClientAdmin.test_topic), "Test poll failed, data error"
            offset_num = 0
            for _par in partitions:
                offset_num += consumer.position(_par)
            self.assertEqual(offset_num, 2), "Test poll failed, offset total error"

    def test_subscribe(self):
        """
        测试订阅topic
        :return:
        """
        topics = [TestClientAdmin.test_topic]
        with Consumer() as consumer:
            consumer.subscribe(topics)
            result = consumer.subscription()
            self.assertTrue(TestClientAdmin.test_topic in result), "Test subscribe topic failed, topic not subscribe."

    def test_topics(self):
        """
        测试获取topics
        :return:
        """
        with Consumer() as consumer:
            result = consumer.get_topics()
            self.assertTrue(TestClientAdmin.test_topic in result), "Test get topics failed, can't get all topics"

    def test_unsubscribe(self):
        """
        测试取消订阅
        :return:
        """
        topics = [TestClientAdmin.test_topic]
        with Consumer() as consumer:
            # 模拟订阅
            consumer.subscribe(topics)
            result = consumer.subscription()
            self.assertTrue(TestClientAdmin.test_topic in result), "Test unsubscribe topic failed, topic not subscribe."
            # 测试取消订阅
            consumer.unsubscribe()
            result = consumer.subscription()
            if result is not None:
                self.assertTrue(TestClientAdmin.test_topic not in result), "Test unsubscribe topic failed, " \
                                                                           "topic not unsubscribe."
