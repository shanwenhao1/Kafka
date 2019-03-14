#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/02/28
# @Author  : Wenhao Shan

from infra.flask.app_init import app
from interfaces.my_log.views import kafka
from interfaces.my_admin.admin_handle import admin


def init_route():
    """
    加载所有路由
    :return:
    """
    app.register_blueprint(kafka, url_prefix="/my_log")
