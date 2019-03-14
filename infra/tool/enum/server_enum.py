#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/01/10
# @Author  : Wenhao Shan

from infra.utils.enum import Enum

ResponseStatus = Enum(
    Success=0,
    Failed=1,
)

ResponseMsg = {
    ResponseStatus.Success: "操作成功",
    ResponseStatus.Failed: "操作失败",
}

InitSer = Enum(
    InitLog="Init Server Log",
    InitZk="Init Server Zookeeper"
)

InquireErr = Enum(
    TimeOut="Time Out",
    OffsetErr="Offset Err"
)
