#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/03/04
# @Author  : Wenhao Shan
# @Dsec    : Wraps of raise ActionError, to handle the exception on the server running
from flask import render_template, jsonify
from functools import wraps
from infra.utils.error import ActionError
from infra.tool.enum.server_enum import ResponseStatus, ResponseMsg


# 自定义err处理装饰器(也可使用flask自带app.errorhandler的创建err handle)
def web_err(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except ActionError as e:
            err_dict = dict()
            err_dict["errMsg"] = e.message
            return render_template("err.html", **err_dict)
    return wrapper


# http request error handle
def action_err(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except ActionError as e:
            res = {
                "errCode": ResponseStatus.Failed,
                "errMsg": e.message,
                "obj": {
                }
            }
            return jsonify(res)
    return wrapper
