#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/11
# @Author  : Wenhao Shan

from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError
from domain.model import TIME_OUT
from infra import log
from infra.conf.kafka_cfg import Config
from infra.utils.error import ActionError
from infra.tool.enum.kafka_enum import KafkaInfo, KafkaErr


class Producer:
    """
    封装kafka-python KafkaProducer
    """

    def __init__(self):
        pass

    def __enter__(self):
        self.cfg = Config().cfg
        self.producer = KafkaProducer(
            bootstrap_servers=self.cfg["serList"],
            # api_version=self.cfg["apiVersion"],
            api_version_auto_timeout_ms=self.cfg["autoVersionTimeout"],
            security_protocol=self.cfg["protocol"],
            sasl_mechanism=self.cfg["mechanism"],
            sasl_kerberos_service_name=self.cfg["kerverosSerName"]
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.producer.close()

    def flush(self):
        """
        调用此方法会使得所有缓存记录变成立即可发送状态.(一般用于send之后, 需要刷新)
        :return:
        """
        try:
            self.producer.flush(timeout=TIME_OUT)
        except KafkaTimeoutError:
            log.tag_error(KafkaInfo.KafkaProducer, "Flush buffered record failed, TimeOut")
            raise ActionError(KafkaErr.FlushFailed)

    def metrics(self):
        """
        获取producer的性能记录(包含各个kafka broker)
        :return:
        """
        performance = self.producer.metrics()
        return performance

    def partition_set_get(self, topic_name: str):
        """
        获取topic的所有分区
        :param topic_name:
        :return: set
        """
        return self.producer.partitions_for(topic_name)

    def send_message(self, topic_name: str, value: bytes, key: str):
        """
        Producer产生数据
        :param topic_name: topic where the message will be published
        :param value: message value
        :param key: key to associate with the message
        :return:
        """
        try:
            result = self.producer.send(topic_name, value=value, key=key.encode("utf-8")).add_errback(self.send_err,
                                                                                                      topic=topic_name,
                                                                                                      value=value,
                                                                                                      key=key)
        except KafkaTimeoutError:
            log.tag_warn(KafkaInfo.KafkaProducer, "Kafka send data timeout, topic: %s, key: %s, msg: %s"
                         % (topic_name, key, value.decode("utf-8")))
            raise ActionError(KafkaErr.SendDataFailed)
        return result

    @staticmethod
    def send_err(topic: str, value: bytes, key: str):
        """
        producer send data failed callback function
        :param topic:
        :param value:
        :param key:
        :return:
        """
        log.tag_error(KafkaInfo.KafkaProducer, "Kafka send data failed, topic: %s, "
                                               "key: %s msg: %s" % (topic, key, value.decode("utf-8")))
        raise ActionError(KafkaErr.SendDataFailed)
