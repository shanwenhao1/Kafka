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

    def get_msg(self, key: str, need_num=20):
        """
        获取消息(倒序查询), 我们用key区分topic下的具体消息
        :param key: msg_key
        :param need_num: need_num is the number of message that you need, if it's not enough, return direct.
        :return:
        """
        # TODO 多次查询, 最好加上timestamp进行筛选
        key_byte = key.encode("utf-8")
        with Consumer(self.group_id) as consumer:
            # 获取key默认分配的分区
            key_partition = self.get_default_partition_by_key(key_byte, consumer)
            partitions = [(self.topic, key_partition)]
            consumer.assign(partitions)
            # 当前的offset(一般是最后)
            last_offset = consumer.position(partitions[0])
            # 如果无记录则直接返回
            if last_offset == 0:
                return []

            not_enough = True
            current_offset = last_offset
            key_records = list()
            while not_enough:
                seek_position = 0 if current_offset <= self.ONCE_GET else current_offset - self.ONCE_GET
                # seek至指定至当前offset前 self.ONCE_GET 位置, 开始顺序poll record
                consumer.seek((self.topic, key_partition), seek_position)
                current_offset = current_offset - self.ONCE_GET
                records = consumer.poll(timeout_ms=1000, max_records=self.ONCE_GET)
                if records == {}:
                    log.tag_error(InquireErr.TimeOut, "Inquire [%s] records failed, time out" % key)
                    raise ActionError(InquireErr.TimeOut)
                records_value = records[consumer.get_topic_partition(self.topic, key_partition)]
                # 筛选出所需key的record
                _records = [_record for _record in records_value if _record.key == key_byte]
                # 该partition下所有records遍历完毕则退出
                if current_offset <= 0:
                    not_enough = False
                if len(_records) < need_num - len(key_records):
                    _records.extend(key_records)
                    key_records = copy.deepcopy(_records)
                    continue
                else:
                    _records[len(_records) - need_num + len(key_records):].extend(key_records)
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


if __name__ == '__main__':
    import time
    from test.test_client_admin import TestClientAdmin
    from domain.model.client_model.client_admin_model import ClientAdmin
    from domain.model.message_model.msg_send_model import MsgSend
    # # 创建测试topic
    # with ClientAdmin() as client:
    #     client.delete_topic(TestClientAdmin.test_topic)
    #     time.sleep(5)
    #     client.create_topic(TestClientAdmin.test_topic)
    msg = ["test msg 1", "test msg 2", "test msg 3"]
    MsgSend(TestClientAdmin.test_topic, "test", msg).send_msg()
    record = MsgInquire(TestClientAdmin.test_topic, "Test_group_id").get_msg("test")
    print("=================", record)
