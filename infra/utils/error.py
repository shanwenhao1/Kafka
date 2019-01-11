#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/01/10
# @Author  : Wenhao Shan


class ActionError(BaseException):
    def __init__(self, message):
        self.message = message

    def __call__(self, *args, **kwargs):
        print("======== {0} ========".format(args))

    def __str__(self, *args, **kwargs):
        error_information = "======== {0} ========".format(self.message)
        print(error_information)
        return error_information

    __repr__ = __str__
