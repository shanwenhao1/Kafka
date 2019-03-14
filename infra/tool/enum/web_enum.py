#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/03/01
# @Author  : Wenhao Shan

from infra.utils.enum import Enum

WebLogTag = Enum(
    UserAccess="User Info Act",
    DbErr="Db Commit Err",
)


UserActionInfo = Enum(
    RegisterSuccess="注册成功, 欢迎: ",
    LoginSuccess="登录成功, 欢迎: ",
    SessionExpire="会话过期, 请重新登录"
)

UserActionErr = Enum(
    RequestErr="请求失败",
    RegisterErr="注册失败",
    LoginErr="登录失败",
    UserExist="用户已存在",
    UserNotExist="用户不存在",
    PasswordFormatErr="密码格式错误, 6-16数字+字母",
    DataBaseErr="数据库操作失败",
    ParamErr="参数错误",
    TopicNotExist="Topic不存在",
    TopicNotBelong="Topic不属于该用户",
    ActionFailed="操作失败",
)


WebInfo = Enum(
    SessionErr="会话错误!!!",
    TopicNotExist="Topic不存在",
)
