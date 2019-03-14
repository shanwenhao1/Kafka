#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/03/02
# @Author  : Wenhao Shan

from flask_login import LoginManager
from infra.flask.app_init import app
from infra.flask.db.base_query import get_user


login_manager = LoginManager()
# login_manager.login_view = "my_log.login"
login_manager.login_message_category = "info"
login_manager.login_message = "Access denied"
# 可以设置None,'basic','strong'以提供不同的安全等级,一般设置strong,如果发现异常会登出用户
login_manager.session_protection = "strong"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id: str):
    """
    注意这里一定要是根据id去查询, 否则会造成session中设置的是id, 但我们查询的不是用的id.
    会一直查询不到, 从而造成session失效
    :param user_id:
    :return:
    """
    user = get_user(user_id)
    return user
