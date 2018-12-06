#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/06
# @Author  : Wenhao Shan

from log.logger import Logger


def debug(msg: str):
    """
    log Debug
    :param msg:
    """
    Logger.debug(msg)


def info(msg: str):
    """
    log Info
    :param msg:
    """
    Logger.info(msg)


def warn(msg: str):
    """
    log Warning
    :param msg:
    """
    Logger.warn(msg)


def error(msg: str):
    """
    log Error
    :param msg:
    """
    Logger.error(msg)


def fatal(msg: str):
    """
    log Fatal error
    :param msg:
    """
    Logger.fatal(msg)


def tag_debug(tag: str, msg: str):
    """
    log Debug with Tag
    :param tag:
    :param msg:
    """
    tag_msg = "【" + tag + "】: " + msg
    debug(tag_msg)


def tag_info(tag: str, msg: str):
    """
    log Info with Tag
    :param tag:
    :param msg:
    """
    tag_msg = "【" + tag + "】: " + msg
    info(tag_msg)


def tag_warn(tag: str, msg: str):
    """
    log Warning with Tag
    :param tag:
    :param msg:
    """
    tag_msg = "【" + tag + "】: " + msg
    warn(tag_msg)


def tag_error(tag: str, msg: str):
    """
    log Error with Tag
    :param tag:
    :param msg:
    """
    tag_msg = "【" + tag + "】: " + msg
    error(tag_msg)
