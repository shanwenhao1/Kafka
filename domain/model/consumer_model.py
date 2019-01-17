#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/11
# @Author  : Wenhao Shan

from kafka import KafkaConsumer
from kafka import TopicPartition
from kafka.errors import IllegalStateError
from infra.conf.kafka_cfg import Config
from infra import log
from infra.utils.error import ActionError
from infra.tool.enum.kafka_enum import KafkaErr, KafkaInfo


class Consumer:
    """
    继承kafka-python KafkaConsumer, 封装自己的方法
    """

    def __init__(self):
        pass

    def __enter__(self):
        self.cfg = Config().cfg
        self.consumer = KafkaConsumer(
            bootstrap_servers=self.cfg["serList"],
            # api_version=self.cfg["apiVersion"],
            api_version_auto_timeout_ms=self.cfg["autoVersionTimeout"],
            security_protocol=self.cfg["protocol"],
            sasl_mechanism=self.cfg["mechanism"],
            sasl_kerberos_service_name=self.cfg["kerverosSerName"]
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.consumer.close()

    def assign(self, partitions: dict):
        """
        手动为当前consumer分配topic分区列表
        :param partitions: 手动分配分区{topic: partition}
        :return:
        """
        _partitions = [TopicPartition(key, value) for key, value in partitions.items()]
        try:
            result = self.consumer.assign(_partitions)
        except IllegalStateError:
            log.tag_error(KafkaInfo.KafkaConsumer, "Manually consumer TopicPartitions error, "
                                                   "Topic Consumer is being in used")
            raise ActionError(KafkaErr.ConsumerInUsed)
        return result

    def assignment(self):
        """
        获取当前consumer分配的topic 分区:
        如果使用assign()手动分配, 则直接返回assign manage 配置
        如果使用subscribe()订阅的话则返回None(无订阅的情况) or set of topic partitions
        :return:
        """
        return self.consumer.assignment()
