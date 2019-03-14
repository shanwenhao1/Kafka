#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/10
# @Author  : Wenhao Shan


from domain.model.message_model.msg_send_model import MsgSend


def msg_send_factory(topic: str, msg_key: str):
    """
    msg send factory
    :param topic:
    :param msg_key:
    :return: the entity of MsgHandle
    """
    msg_send = MsgSend(topic, msg_key)
    return msg_send
