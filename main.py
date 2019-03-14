#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/01/10
# @Author  : Wenhao Shan

import pymysql
from infra import log
from infra.tool.enum.server_enum import InitSer
from infra.flask.app_init import app
from infra.flask.db import init_db
from interfaces.server import init_route

# 将所有调用的import MySQLdb导入至pymysql
pymysql.install_as_MySQLdb()


Web_Ip = "192.168.1.89"
Web_Port = "5000"


def main():
    """
    function main
    :return:
    """
    log.tag_info(InitSer.InitLog, "Init Log okay")
    # 数据库初始化
    init_db()
    # 加载所有路由
    init_route()
    app.run(host=Web_Ip, port=Web_Port, debug=True)


if __name__ == '__main__':
    main()
