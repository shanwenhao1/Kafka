#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/11
# @Author  : Wenhao Shan

from kafka import KafkaProducer
from infra.conf.kafka_cfg import Config


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
            api_version=self.cfg["apiVersion"],
            security_protocol=self.cfg["protocol"],
            sasl_mechanism=self.cfg["mechanism"],
            sasl_kerberos_service_name=self.cfg["mechanism"],
            )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.producer.close()
