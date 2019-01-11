#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/01/10
# @Author  : Wenhao Shan

from infra import log
from infra.log.logger import InitLog
from infra.tool.enum.server_enum import InitSer


def main():
    """
    function main
    :return:
    """
    log.tag_info(InitSer.InitLog, "Init Log okay")
    from infra.conf.kafka_cfg import Config
    print(Config(), Config(), Config.cfg)
    log.info("----=====1")
    log.info("----=====2")
    log.info("----=====3")


if __name__ == '__main__':
    main()
