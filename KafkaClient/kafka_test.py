#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/06
# @Author  : Wenhao Shan

from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError
from conf.config import Config

TestTopic = "test"
KafkaServer = ["192.168.1.89:9092", "192.168.1.89:9093", "192.168.1.89:9094"]

producer = KafkaProducer(
    bootstrap_servers=KafkaProducer
)

consumer = KafkaConsumer(TestTopic)

for msg in consumer:
    print(msg)
