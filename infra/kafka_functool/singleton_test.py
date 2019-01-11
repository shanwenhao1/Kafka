#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/01/10
# @Author  : Wenhao Shan
# @DSC     : test the singleton wrapper

from unittest import TestCase
from infra.kafka_functool.singleton import singleton


class SingletonTest(TestCase):
    """
    单例测试
    """

    @singleton
    class Foo:
        """
        单例使用示例
        """

        def __new__(cls, *args, **kwargs):
            cls.x = 10
            cls.y = 1
            return object.__new__(cls)

        def __init__(self):
            assert self.x == 10
            self.x = 15

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_singleton(self):
        assert self.Foo() == self.Foo()
        assert self.Foo().x == 15
        self.Foo().x = 20
        assert self.Foo().x == 20
        assert self.Foo().y == 1
        self.Foo().y = 2
        assert self.Foo().y == 2
