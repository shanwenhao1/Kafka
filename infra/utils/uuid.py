#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/02/27
# @Author  : Wenhao Shan
import uuid


def new_uuid():
    """
    generate new uuid
    :return: str
    """
    new_id = uuid.uuid1()
    return new_id.__str__()
