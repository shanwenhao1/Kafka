#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/01/16
# @Author  : Wenhao Shan
import sys
import inspect
import unittest
from infra.utils.error import for_code, ServerResponseError


class TestError(ServerResponseError):
    err_no = -999
    message = "Test Error"
    description = "Test error"


class ErrorTest(unittest.TestCase):
    """
    Error test
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def raise_error():
        raise for_code(-999)("Test '{}' failed with test '{}'.".format("test_error", "test_error"))

    def test_for_code(self):
        print(for_code(-999).__bases__)
        self.assertTrue(issubclass(for_code(-999), ServerResponseError)), "Test Error Failed!!!"
        try:
            self.raise_error()
            self.assertTrue(False), "Raise Error Failed!"
        except ServerResponseError:
            print("raise error succeed")
