#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/11
# @Author  : Wenhao Shan

from kafka import KafkaAdminClient
from infra.conf.kafka_cfg import Config
from domain.model import TIME_OUT


class ClientAdmin:
    """
    封装kafka-python KafkaAdminClient
    """

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

    def create_topic(self, topic_name: str):
        """
        在集群中创建新的topic
        :param topic_name:
        :return:
        """
        topic_list = [topic_name]
        # TODO change topic_list to a object
        self.admin_client.create_topics(topic_list, timeout_ms=TIME_OUT)

    def delete_topic(self, topic_name: str):
        """
        删除集群中的topic
        :param topic_name:
        :return:
        """
        topic_list = [topic_name]
        self.admin_client.delete_topics(topic_list, timeout_ms=TIME_OUT)
