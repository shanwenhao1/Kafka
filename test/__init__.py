#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/01/10
# @Author  : Wenhao Shan
# @DSC     : Test Project
import os
import unittest
from test.test_client_admin import TestClientAdmin
from test.test_consumer import TestConsumer
from test.test_producer import TestProducer2


def test_main():
    """
    运行所有测试
    :return:
    """
    # case_path = os.getcwd()
    # all_case = unittest.TestSuite()
    # all_case.addTests(unittest.defaultTestLoader.discover(case_path, pattern="test*"))
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(all_case)

    # all_case = unittest.TestSuite()
    # print("========", unittest.TestLoader().loadTestsFromNames(['test_client_admin.TestClientAdmin',
    #                                                             'test_client_admin.TestClientAdmin2']))
    # all_case.addTests(unittest.TestLoader().loadTestsFromNames(['test_client_admin.TestClientAdmin',
    #                                                             'test_client_admin.TestClientAdmin2']))
    all_case = unittest.TestSuite()
    case_list = [TestClientAdmin, TestProducer2, TestConsumer]
    for case in case_list:
        case_all = unittest.TestLoader().loadTestsFromTestCase(case)
        all_case.addTests(case_all)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(all_case)


if __name__ == '__main__':
    test_main()
