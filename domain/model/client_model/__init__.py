#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22
# @Author  : Wenhao Shan
# @DSC     : Base Model of Kafka operation, include admin-client, producer-client, consumer-client

TIME_OUT = 5000             # 操作超时时间, 单位ms
TIME_OUT_ADMIN = 10000      # Admin操作超时时间(由于admin执行的操作一般较为耗时, 应根据情况设定)
