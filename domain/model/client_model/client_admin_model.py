#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/11
# @Author  : Wenhao Shan

from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError
from infra.conf.kafka_cfg import Config
from infra import log
from infra.tool.enum.kafka_enum import KafkaInfo, KafkaErr
from infra.utils.error import ActionError
from domain.model.client_model import TIME_OUT_ADMIN

# TODO Kafka-python Admin Create Topic has a error, wait for official fix it.
"""
    if you want use anyway, you can change your local file in this way:
    https://github.com/dpkp/kafka-python/commit/1a31be52ec012dfa0ef5079ff9982e01408a8fe1
    
    topic_error_tuples = (response.topic_errors if hasattr(response, 'topic_errors') else response.topic_error_codes)
    # DeleteTopicsResponse returns topic_error_codes rather than topic_errors
    for topic, error_code in map(lambda e: e[:2], topic_error_tuples):
"""


class ClientAdmin:
    """
    封装kafka-python KafkaAdminClient
    """
    Num_Partitions = 3
    Replication_Factor = 3

    def __init__(self):
        pass

    def __enter__(self):
        self.cfg = Config().cfg
        self.admin_client = KafkaAdminClient(
            bootstrap_servers=self.cfg["serList"],
            # api_version=self.cfg["apiVersion"],
            api_version_auto_timeout_ms=self.cfg["autoVersionTimeout"],
            security_protocol=self.cfg["protocol"],
            sasl_mechanism=self.cfg["mechanism"],
            sasl_kerberos_service_name=self.cfg["kerverosSerName"]
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.admin_client.close()

    @staticmethod
    def new_topic(topic_name: str,):
        """
        generate new topic object
        :return:
        """
        return NewTopic(name=topic_name, num_partitions=ClientAdmin.Num_Partitions,
                        replication_factor=ClientAdmin.Replication_Factor,
                        replica_assignments=None, topic_configs=None)

    def create_topic(self, topic_name: str):
        """
        在集群中创建新的topic(topic配置采用默认模式)
        :param topic_name:
        :return:
        """
        topic_list = [self.new_topic(topic_name)]
        try:
            response = self.admin_client.create_topics(topic_list, timeout_ms=TIME_OUT_ADMIN)
        except TopicAlreadyExistsError:
            log.tag_error(KafkaInfo.KafkaAdmin, "Topic [%s] already exist! Create Failed !" % topic_name)
            raise ActionError(KafkaErr.TopicExist)
        return response

    def delete_topic(self, topic_name: str):
        """
        删除集群中的topic
        :param topic_name:
        :return:
        """
        topic_list = [topic_name]
        try:
            self.admin_client.delete_topics(topic_list, timeout_ms=TIME_OUT_ADMIN)
        except UnknownTopicOrPartitionError as e:
            log.tag_error(KafkaInfo.KafkaAdmin, "Topic [%s] not exist! Don't need delete" % topic_name)
            raise ActionError(KafkaErr.TopicNotExist)

    def create_partition(self):
        """
        为现有主题创建其他分区
        :return:
        """

    def list_consumer_groups(self):
        """
        列出集群中的消费者集群
        :return:
        """
        return self.admin_client.list_consumer_groups()

    # TODO 留存一些函数未封装, 后续如果需要再进行封装
