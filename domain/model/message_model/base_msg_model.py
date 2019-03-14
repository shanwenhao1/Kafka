#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22
# @Author  : Wenhao Shan

import json


class BaseMsg:
    """
    Kafka message base class
    """

    def __init__(self, topic: str, msg_key: str):
        self.topic = topic
        self.msg_key = msg_key

    def get_json(self):
        """
        获取json
        :return:
        """
        key_json = self.__dict__
        return key_json


if __name__ == '__main__':
    test_json = BaseMsg("topic", "msg_key").get_json()
    test_str = json.dumps(test_json)
    base_msg = BaseMsg(**json.loads(test_str))
    print(base_msg.topic)
