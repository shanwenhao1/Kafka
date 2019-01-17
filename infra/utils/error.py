#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/01/10
# @Author  : Wenhao Shan

from __future__ import absolute_import

import inspect
import sys


class BaseError(RuntimeError):
    retriable = False
    # whether metadata should be refreshed on error
    invalid_metadata = False

    def __str__(self):
        if not self.args:
            return self.__class__.__name__
        return '{0}: {1}'.format(self.__class__.__name__,
                                 super(BaseError, self).__str__())


class ServerResponseError(BaseError):
    err_no = None
    message = None
    description = None

    def __str__(self):
        """Add errno to standard ServerResponseError str"""
        return '[Error {0}] {1}'.format(
            self.err_no,
            super(ServerResponseError, self).__str__())


class UnknownError(ServerResponseError):
    err_no = -1
    message = "Unknown Error"
    description = "An unexpected server error"


def _iter_broker_errors():
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and issubclass(obj, ServerResponseError) and obj != ServerResponseError:
            yield obj


kafka_errors = dict([(x.err_no, x) for x in _iter_broker_errors()])


def for_code(error_code):
    return kafka_errors.get(error_code, UnknownError)


class ActionError(BaseException):
    """
    user action error
    """

    def __init__(self, message):
        self.message = message

    def __call__(self, *args, **kwargs):
        print("======== {0} ========".format(args))

    def __str__(self, *args, **kwargs):
        error_information = "======== {0} ========".format(self.message)
        print(error_information)
        return error_information

    __repr__ = __str__
