#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22
# @Author  : Wenhao Shan

import json


class BaseMsg:
    """
    Kafka message base class
    """

    def __init__(self, topic: str, msg_key: str, msg: str or list):
        self.topic = topic
        self.msg_key = msg_key
        self.msg = msg

    def get_json(self):
        """
        获取json
        :return:
        """
        key_json = self.__dict__
        print(key_json)
        return key_json


if __name__ == '__main__':
    test_json = BaseMsg("topic", "msg_key", "msg_value").get_json()
    test_str = json.dumps(test_json)
    base_msg = BaseMsg(**json.loads(test_str))
    print(base_msg.topic)
