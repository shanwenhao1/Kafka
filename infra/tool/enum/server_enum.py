#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/01/10
# @Author  : Wenhao Shan

from infra.utils.enum import Enum

InitSer = Enum(
    InitLog="Init Server Log",
    InitZk="Init Server Zookeeper"
)

InquireErr = Enum(
    TimeOut="Time Out",
    OffsetErr="Offset Err"
)
