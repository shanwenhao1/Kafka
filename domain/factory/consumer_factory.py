#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/10
# @Author  : Wenhao Shan


from domain.model.message_model.msg_inquire_model import MsgInquire


def msg_get_factory(topic: str, group_id: str):
    """
    msg inquire factory
    :param topic:
    :param group_id:
    :return:
    """
    msg_get = MsgInquire(topic, group_id)
    return msg_get
