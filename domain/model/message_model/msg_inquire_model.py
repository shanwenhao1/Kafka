#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22
# @Author  : Wenhao Shan
# @DSC     : Inquire message from kafka cluster

import copy
from kafka.partitioner import DefaultPartitioner
from infra.utils.error import ActionError
from infra import log
from infra.tool.enum.server_enum import InquireErr
from domain.model.client_model.consumer_model import Consumer


class MsgInquire:
    """
    查询消息
    """
    ONCE_GET = 1000

    def __init__(self, topic: str, group_id: str = None):
        self.topic = topic
        self.group_id = group_id

    def get_msg_with_offset(self, key: str, offset: int = 0, need_num: int = 20, timestamp: int = 0):
        """
        获取消息(倒序查询), 我们用key区分topic下的具体消息
        :param key:
        :param offset:
        :param need_num:
        :param timestamp:
        :return:
        """
        key_byte = key.encode("utf-8")
        with Consumer(self.group_id) as consumer:
            # 获取key默认分配的分区
            key_partition = self.get_default_partition_by_key(key_byte, consumer)
            partitions = [(self.topic, key_partition)]
            consumer.assign(partitions)
            # seek offset to the end
            consumer.seek_many(partitions, is_begin=False)
            last_offset = consumer.position(partitions[0])
            if last_offset == 0:
                return []
            # 如果无记录则直接返回
            if offset > last_offset:
                raise ActionError(InquireErr.OffsetErr)
            current_offset = offset
            records = self._get_msg_by_key(consumer, key, current_offset, key_partition, need_num, timestamp)
        return records

    def _get_msg_by_key(self, consumer: Consumer, key: str, offset: int, key_partition: int, need_num: int, timestamp: int):
        """
        获取消息(倒序查询), 我们用key区分topic下的具体消息
        :param consumer:
        :param key:
        :param offset:
        :param key_partition:
        :param need_num: need_num is the number of message that you need, if it's not enough, return direct.
        :param timestamp: if timestamp not equal to 0, then all inquire records need recorded before timestamp
        :return:
        """
        key_byte = key.encode("utf-8")

        not_enough = True
        current_offset = offset
        key_records = list()
        while not_enough:
            if current_offset <= self.ONCE_GET:
                seek_position = 0
                max_record = current_offset if current_offset != 0 else self.ONCE_GET
            else:
                seek_position = current_offset - self.ONCE_GET
                max_record = self.ONCE_GET
            # seek至指定position 开始poll record(顺序poll的, 因此需要处理下再返回)
            consumer.seek((self.topic, key_partition), seek_position)
            records = consumer.poll(timeout_ms=10000, max_records=max_record)
            if records == {}:
                log.tag_error(InquireErr.TimeOut, "Inquire [%s] records failed, time out" % key)
                raise ActionError(InquireErr.TimeOut)
            records_value = records[consumer.get_topic_partition(self.topic, key_partition)]
            # 筛选出所需key的record
            if timestamp == 0:
                _records = [_record for _record in records_value if _record.key == key_byte]
            else:
                _records = [_record for _record in records_value if _record.key == key_byte and _record.timestamp <= timestamp]
            # 该partition下所有records遍历完毕则退出
            current_offset = current_offset - self.ONCE_GET
            if current_offset <= 0:
                not_enough = False
            if len(_records) < need_num - len(key_records):
                _records.extend(key_records)
                key_records = copy.deepcopy(_records)
                continue
            else:
                _records = _records[len(_records) - need_num + len(key_records):]
                _records.extend(key_records)
                key_records = copy.deepcopy(_records)
                not_enough = False

        return key_records

    def get_default_partition_by_key(self, key: bytes, consumer: Consumer):
        """
        根据key获取指定的topic分区,
        注意: 由于available_partitions_for_topic属于kafka, 我们获取不到可用的分区列表, 但由于当key不为None时,
        可用分区参数没有用到(详情请见DefaultPartitioner), 因此key必须不为None
        :param key:
        :param consumer: Consumer实例
        :return:
        """
        # 获取topic的所有分区
        partition = consumer.partition_for_topic(self.topic)
        par_list = [_par for _par in partition]
        choice_partition = DefaultPartitioner().__call__(key, par_list, par_list)
        return choice_partition
