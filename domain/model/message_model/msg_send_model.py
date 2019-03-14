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

    def __init__(self, topic: str, msg_key: str):
        super(MsgSend, self).__init__(topic, msg_key)

    def send_msg(self, msg: str):
        """
        发送msg
        :param msg:
        :return:
        """
        with Producer() as producer:
            producer.send_message(self.topic, msg.encode("utf-8"), self.msg_key)

    def send_msg_mul(self, msg: list):
        """
        发送msg(多条)
        :param msg:
        :return:
        """
        with Producer() as producer:
            for msg in msg:
                producer.send_message(self.topic, msg.encode("utf-8"), self.msg_key)

