#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/11
# @Author  : Wenhao Shan

from kafka import KafkaConsumer
from infra.conf.kafka_cfg import Config


class Consumer(KafkaConsumer):
    """
    继承kafka-python KafkaConsumer, 封装自己的方法
    """

    def __init__(self):
        super(Consumer, self).__init__()
        self.cfg = Config().cfg
        self.consumer = KafkaConsumer(
            bootstrap_servers=self.cfg["serList"],
            api_version=self.cfg["apiVersion"],
            security_protocol=self.cfg["protocol"],
            sasl_mechanism=self.cfg["mechanism"],
            sasl_kerberos_service_name=self.cfg["mechanism"],
            )
