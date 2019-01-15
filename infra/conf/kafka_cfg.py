#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/01/10
# @Author  : Wenhao Shan

from infra.utils.error import ActionError
from infra.conf.config import ZkConfig
from infra.tool.enum.cfg_enum import KaCfgType
from infra.kafka_functool.singleton import singleton


# 本地kafka config,
# apiVersion可由kafka-python内部函数自动获取, 不使用apiVersion时则需要考虑网络延时合理配置autoVersionTimeout参数.
# 使用配置的话只是提高一点性能(注意: 如果需要配置一定确保正确)
KafkaConfig = {
    "serList":              ["192.168.1.89:9092", "192.168.1.89:9093", "192.168.1.89:9094"],
    "apiVersion":           [1, 0, 0],
    "autoVersionTimeout":   2000,
    "protocol":             "SASL_PLAINTEXT",
    "mechanism":            "GSSAPI",
    "kerverosSerName":      "kafka"
}


def get_kafka_cfg():
    """
    获取kafka访问配置
    :return:
    """
    try:
        # 使用zk获取配置
        cfg = ZkConfig("test", "ts1245", "/kafka").get_config(KaCfgType.KafkaCfg)
    except ActionError:
        # zk服务不可用时, 采用本地config配置
        cfg = KafkaConfig
    # cfg 中的apiVersion需要单独处理
    try:
        cfg["apiVersion"] = tuple(cfg["apiVersion"])
    except Exception:
        raise ActionError("Kafka config error!!!")
    return cfg


@singleton
class Config:
    """
    配置单例(防止重复查询zk配置), 如果需要考虑不重启服务更改配置, 则不应采用单例模式
    """
    def __new__(cls, *args, **kwargs):
        cls.cfg = get_kafka_cfg()
        return object.__new__(cls)

    def __init__(self):
        pass
