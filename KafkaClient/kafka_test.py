#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/06
# @Author  : Wenhao Shan

from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError
# from conf.config import Config

TestTopic = "test"
KafkaServer = ["192.168.1.89:9092", "192.168.1.89:9093", "192.168.1.89:9094"]

producer = KafkaProducer(
    bootstrap_servers=KafkaServer,
    api_version=(2, 11, 2),
    security_protocol="SASL_PLAINTEXT",
    sasl_mechanism='GSSAPI',
    sasl_kerberos_service_name='kafka',
)
print("====================")
future = producer.send(TestTopic, b"raw_bytes")

try:
    record_metdata = future.get(timeout=10)
    print(record_metdata.topic)
    print(record_metdata.partition)
    print(record_metdata.offset)
except KafkaError:
    print(KafkaError)


# consumer = KafkaConsumer(TestTopic)
#
# for msg in consumer:
#     print(msg)
