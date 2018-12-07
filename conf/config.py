#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/06
# @Author  : Wenhao Shan
# DSC      : if you want to make this project start, please make sure that your Zookeeper server already started.
#            Then you can load your Kafka conf !!!

import json
import requests
from utils.error import ActionError
from Kafka_tool.enum.cfg_enum import KaCfgType
from Kafka_tool.enum.status_enum import ActionStatus

# Zookeeper服务地址
ZkAddress = "http://localhost:8081/zk_node/"


class BaseConfig(object):
    """
    存放基础配置的zk信息基类
    """
    zkUser = "zkUser"
    zkPassword = "zkPassword"
    zkNode = "zkNode"

    def __init__(self):
        self.base_config = dict()
        # 添加Kafka zk连接信息
        self.base_config[KaCfgType.KafkaCfg] = {
            self.zkUser: "test",               # 用户名
            self.zkPassword: "ts1245",         # 密码
            self.zkNode: "/kafka",             # 节点值
        }


class Config(BaseConfig):
    """
    获取zk config 配置
    """

    def __init__(self):
        super(Config, self).__init__()
        self.headers = {"content-type": 'application/json'}

    def get_config(self, cfg_type: str):
        """
        根据cfg_type参数获取相应的zk配置
        :param cfg_type:
        :return:
        """
        req_data = {
            "username": self.base_config[cfg_type][self.zkUser],
            "password": self.base_config[cfg_type][self.zkPassword],
            "zkPath": self.base_config[cfg_type][self.zkNode]
        }
        # 请求ZooKeeper服务器, 获取相应的节点配置信息
        try:
            req = requests.post(ZkAddress, data=req_data)
            resp = req.json()
        except:
            raise ActionError("Zk Server Error, Init Kafka server error!!!")

        if resp["status"] != ActionStatus.ActionSuccess:
            raise ActionError(resp["errMsg"])
        conf = resp["zkData"]
        return conf


if __name__ == '__main__':
    cfg = Config().get_config(KaCfgType.KafkaCfg)
    print(cfg)
