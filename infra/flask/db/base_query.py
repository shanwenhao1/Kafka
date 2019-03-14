#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/02/27
# @Author  : Wenhao Shan
from infra.flask.db.models import User


def get_user(user_id: str):
    """
    查询user
    :param user_id:
    :return:
    """
    user = User.query.filter_by(id=user_id).first()
    return user


def get_username(username: str):
    """
    查询user, 根据username查询
    :param username:
    :return:
    """
    user = User.query.filter_by(name=username).first()
    return user
