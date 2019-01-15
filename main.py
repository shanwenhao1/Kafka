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
    # from domain.model.client_admin_model import ClientAdmin
    # with ClientAdmin() as client:
    #     pass


if __name__ == '__main__':
    main()
