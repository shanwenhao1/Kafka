#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/01/10
# @Author  : Wenhao Shan
from infra.log.logger import Log


def debug(msg: str):
    """
    log Debug
    :param msg:
    """
    Log.debug(msg)


def info(msg: str):
    """
    log Info
    :param msg:
    """
    Log.info(msg)


def warn(msg: str):
    """
    log Warning
    :param msg:
    """
    Log.warn(msg)


def error(msg: str):
    """
    log Error
    :param msg:
    """
    Log.error(msg)


def fatal(msg: str):
    """
    log Fatal error
    :param msg:
    """
    Log.fatal(msg)


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
