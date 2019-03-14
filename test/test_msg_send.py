#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/03/08
# @Author  : Wenhao Shan

import json
import unittest
import urllib.request
from infra.utils.time_utils import get_now_time, datetime_to_str, get_now_time_timestamp
from interfaces.my_log.route_component.kafka_action.msg_send import md5_check


class TestMsgHandle(unittest.TestCase):
    """
    Test flask MsgHandle
    """

    def setUp(self):
        self.request_url = "http://192.168.1.89:5000/my_log/send"
        self.headers = {'Content-Type': 'application/json'}

    def tearDown(self):
        pass

    def test_get_msg(self):
        """
        :return:
        """
        from domain.service.msg_service import inquire_msg
        result = inquire_msg("test", "web group", "test_key", offset=0)
        print("-----------------", result)

    def test_send_msg(self):
        """
        test send message
        :return:
        """
        for i in range(1):
            now_time = get_now_time_timestamp()
            md5_verify = md5_check("622b6aa3-4562-11e9-b760-000c29813bbb", now_time)
            req_data = {
                # "user": "test",
                "username": "test",
                "verify": md5_verify,
                "timestamp": now_time,
                "topic": "test",
                "msgKey": "test_key",
                "msg": "test flask send msg" + datetime_to_str(get_now_time())
            }
            req_data_dump = json.dumps(req_data)
            request = urllib.request.Request(url=self.request_url, headers=self.headers, data=req_data_dump.encode("utf-8"))
            response = urllib.request.urlopen(request)
            res = json.loads(response.read())
            print("---------===", res)
            self.assertEqual(res["errCode"], 0), "测试发送message失败!!!"
