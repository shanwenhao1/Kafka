#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/01/16
# @Author  : Wenhao Shan
from infra.utils.enum import Enum

KafkaInfo = Enum(
    KafkaAdmin="Kafka Admin",
    KafkaProducer="Kafka Producer",
    KafkaConsumer="Kafka Consumer",
)


KafkaErr = Enum(
    UnknownErr="Unknown Error",
    ParameterError="Parameter Error",
    TopicExist="Topic Already Exist",
    TopicNotExist="Topic Not Exist",
    TopicPartitionNotExist="Topic Partition Not Exist",
    FlushFailed="Flush Buffered Record Failed",
    SendDataFailed="Send Data Failed",
    ConsumerInUsed="Consumer Is Being In Used",
    NotSupport="Not Support Now",
    GetOffsetFailed="Get Offset Failed",
    CommitOffsetFailed="Commit Offset Failed",
)
