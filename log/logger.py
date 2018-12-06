#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/06
# @Author  : Wenhao Shan

import logging.handlers
from log.log_cfg import Log_File, Id_Simple_Format

# cfg_dict = LOGGING
# logging.config.dictConfig(cfg_dict)
# Logger = logging.getLogger(Log_File)


Logger = logging.getLogger("ZK Admin")
Logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(Id_Simple_Format)

# 文件日志
file_handler = logging.handlers.RotatingFileHandler(Log_File, maxBytes=1024 * 1024 * 5, backupCount=5, encoding="utf-8")
file_handler.formatter = formatter

# # 控制台日志
# console_handler = logging.StreamHandler(sys.stdout)
# console_handler.formatter = formatter

Logger.addHandler(file_handler)
# Logger.addHandler(console_handler)


if __name__ == '__main__':
    Logger.info("test log")
