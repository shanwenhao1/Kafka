#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/01/10
# @Author  : Wenhao Shan

import logging.handlers
from infra.log.log_cfg import Log_File, Id_Simple_Format

# cfg_dict = LOGGING
# logging.config.dictConfig(cfg_dict)
# Logger = logging.getLogger(Log_File)


def InitLog():
    """
    初始化log
    :return:
    """
    logger = logging.getLogger("kafka")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(Id_Simple_Format)

    # 文件日志
    file_handler = logging.handlers.RotatingFileHandler(Log_File, maxBytes=1024 * 1024 * 5, backupCount=5, encoding="utf-8")
    file_handler.formatter = formatter

    # # 控制台日志
    # console_handler = logging.StreamHandler(sys.stdout)
    # console_handler.formatter = formatter

    logger.addHandler(file_handler)
    # Logger.addHandler(console_handler)
    return logger


Log = InitLog()

if __name__ == '__main__':
    InitLog().info("test log")
