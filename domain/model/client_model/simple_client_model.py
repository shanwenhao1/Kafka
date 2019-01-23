#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/11
# @Author  : Wenhao Shan

from kafka import KafkaClient as SimpleClient
from infra.conf.kafka_cfg import Config
from infra import log
from infra.tool.enum.kafka_enum import KafkaInfo, KafkaErr
from infra.utils.error import ActionError

# TODO KafkaClient will remove in future release, so remain to add need function in the future


class Client:
    """
    封装kafka-python KafkaClient,
    """

    def __init__(self):
        pass

    def __enter__(self):
        self.cfg = Config().cfg
        self.client = SimpleClient(
            bootstrap_servers=self.cfg["serList"],
            # api_version=self.cfg["apiVersion"],
            api_version_auto_timeout_ms=self.cfg["autoVersionTimeout"],
            security_protocol=self.cfg["protocol"],
            sasl_mechanism=self.cfg["mechanism"],
            sasl_kerberos_service_name=self.cfg["kerverosSerName"]
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def add_topic(self, topic_name: str):
        """
        :param topic_name:
        :return:
        """
