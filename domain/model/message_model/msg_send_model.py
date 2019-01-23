#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22
# @Author  : Wenhao Shan
# @DSC     : Send message to kafka cluster

from domain.model.message_model.base_msg_model import BaseMsg
from domain.model.client_model.producer_model import Producer


class MsgSend(BaseMsg):
    """
    发送消息
    """

    def __init__(self, topic: str, msg_key: str, msg: str or list):
        super(MsgSend, self).__init__(topic, msg_key, msg)

    def send_msg(self):
        """
        发送msg
        :return:
        """
        with Producer() as producer:
            if type(self.msg) is list:
                for msg in self.msg:
                    producer.send_message(self.topic, msg.encode("utf-8"), self.msg_key)
            else:
                producer.send_message(self.topic, self.msg.encode("utf-8"), self.msg_key)

