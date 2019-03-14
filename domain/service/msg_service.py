#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22
# @Author  : Wenhao Shan
# @DSC     : service of producer model

from infra.utils.time_utils import timestamp_to_datetime, datetime_to_str, get_now_time_timestamp
from domain.factory.producer_factory import msg_send_factory
from domain.factory.consumer_factory import msg_get_factory


def send_msg(topic: str, msg_key: str, msg: str):
    """
    向kafka发送消息的领域服务
    :param topic:
    :param msg_key:
    :param msg:
    :return:
    """
    msg_fac = msg_send_factory(topic, msg_key)
    msg_fac.send_msg(msg)


def send_msg_mul(topic: str, msg_key: str, msg: list):
    """
    一次性向kafka发送多条消息的领域服务
    :param topic:
    :param msg_key:
    :param msg:
    :return:
    """
    msg_fac = msg_send_factory(topic, msg_key)
    msg_fac.send_msg_mul(msg)


def inquire_msg(topic: str, group_id: str, key: str, offset: int = 0):
    """
    查询消息
    :param topic:
    :param group_id:
    :param key:
    :param offset:
    :return:
    """
    msg_inquire = msg_get_factory(topic, group_id)
    msg_records = msg_inquire.get_msg_with_offset(key=key, offset=offset)
    msgs = list()
    for _record in msg_records:
        _rec_info = {
            "topic": _record.topic,
            "offset": _record.offset,
            "msgTime": datetime_to_str(timestamp_to_datetime(_record.timestamp)),
            "message": _record.value.decode("utf-8")
        }
        msgs.append(_rec_info)
    # 倒序返回
    msgs.reverse()
    return msgs


def inquire_msg_time_limit(topic: str, group_id: str, key: str, offset: int = 0, timestamp: int = 0):
    """
    查询消息(加上时间限制, 某个时间点之前的消息)
    :param topic:
    :param group_id:
    :param key:
    :param offset:
    :param timestamp:
    :return:
    """
    msg_inquire = msg_get_factory(topic, group_id)
    msg_records = msg_inquire.get_msg_with_offset(key=key, offset=offset, timestamp=timestamp)
    msgs = list()
    for _record in msg_records:
        _rec_info = {
            "topic": _record.topic,
            "offset": _record.offset,
            "msgTime": datetime_to_str(timestamp_to_datetime(_record.timestamp)),
            "message": _record.value.decode("utf-8")
        }
        msgs.append(_rec_info)
    # 倒序返回
    msgs.reverse()
    return msgs
