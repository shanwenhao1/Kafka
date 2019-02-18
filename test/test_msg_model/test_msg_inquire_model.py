#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/15
# @Author  : Wenhao Shan
# @DSC     : test of msg inquire

import unittest
from infra.utils.time_utils import get_now_time_timestamp, get_another_time, time_str_to_timestamp, datetime_to_str
from test.test_client_model.test_client_admin import TestClientAdmin
from domain.model.message_model.msg_send_model import MsgSend
from domain.model.message_model.msg_inquire_model import MsgInquire


class TestMsgInquire(unittest.TestCase):
    """
    Test of Msg inquire
    """

    def setUp(self):
        self.base_msg = "test msg"
        TestClientAdmin.mock_test_topic(TestClientAdmin.test_topic)
        msg = [self.base_msg + str(i) for i in range(0, 100)]
        MsgSend(TestClientAdmin.test_topic, "test", msg).send_msg()

    def tearDown(self):
        TestClientAdmin.mock_clear_topic(TestClientAdmin.test_topic)

    def test_get_msg_with_offset(self):
        """
        测试查询record
        :return:
        """
        msg_inquire = MsgInquire(TestClientAdmin.test_topic, "Test_group_id")
        records = msg_inquire.get_msg_with_offset("test")
        self.assertEqual(records[0].value.decode("utf-8"), self.base_msg + '80'), "Test msg inquire failed, " \
                                                                                  "msg error!!!"
        self.assertEqual(records[-1].value.decode("utf-8"), self.base_msg + "99"), "Test msg inquire failed, " \
                                                                                   "msg error!!!"

        records = msg_inquire.get_msg_with_offset("test", offset=40)
        self.assertEqual(records[0].value.decode("utf-8"), self.base_msg + '20'), "Test msg inquire failed, " \
                                                                                  "msg error!!!"
        self.assertEqual(records[-1].value.decode("utf-8"), self.base_msg + "39"), "Test msg inquire failed, " \
                                                                                   "msg error!!!"

        # 测试timestamp参数
        timestamp = get_now_time_timestamp(need_ms=True)
        records = msg_inquire.get_msg_with_offset("test", timestamp=timestamp)
        self.assertEqual(len(records), 20), "Test msg inquire failed, get msg filter by timestamp failed!!!"
        self.assertEqual(records[-1].value.decode("utf-8"), self.base_msg + "99"), "Test msg inquire failed, get msg " \
                                                                                   "filter by timestamp failed!!!"
        new_timestamp = records[0].timestamp
        records = msg_inquire.get_msg_with_offset("test", timestamp=new_timestamp)
        self.assertTrue(records[0].timestamp < new_timestamp), "Test msg inquire failed, get wrong record!!!"
        self.assertEqual(records[-1].timestamp, new_timestamp), "Test msg inquire failed, record timestamp error!!!"
