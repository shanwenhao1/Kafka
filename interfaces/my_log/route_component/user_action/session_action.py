#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/02/27
# @Author  : Wenhao Shan
from datetime import timedelta
from flask import render_template, session, flash
from flask_login import login_user, logout_user
from infra import log
from infra.flask.app_init import db, app
from infra.flask.db.base_query import get_username
from infra.flask.db.models import User
from infra.flask.db.db_tool import commit
from infra.utils.word_check import pass_word_check
from infra.utils.md5 import generate_md5
from infra.utils.error import ActionError
from infra.tool.enum.web_enum import UserActionErr, UserActionInfo, WebLogTag


def check_session(username: str):
    """
    判断用户是否已登录
    :param username:
    :return:
    """
    if username in session:
        return True
    else:
        return False


class UserAction:
    """
    用户操作类
    """

    def __init__(self, request):
        self.request = request
        self.context = dict()

    @staticmethod
    def user_login(user):
        """
        登入并设置session的静态方法
        :param user:
        :return:
        """
        # 登录并设置cookies30分钟后过期
        login_user(user)
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)
        log.tag_info(WebLogTag.UserAccess, "User: %s login in" % user.name)

    def register(self):
        """
        用户注册
        :return:
        """
        if self.request.method == "GET":
            return render_template("register.html", **self.context)
        if self.request.method != "POST":
            raise ActionError(UserActionErr.RequestErr)
        par_dict = self.request.form.to_dict()
        user_name = par_dict["user_name"]
        password = par_dict["password"]
        email = par_dict["email"]
        sex = par_dict["sex"]

        # check name has been registered or not
        record = get_username(user_name)
        if record is not None:
            self.context["errMsg"] = UserActionErr.UserExist
            return render_template("register.html", **self.context)

        # check password
        if not pass_word_check(password):
            self.context["errMsg"] = UserActionErr.PasswordFormatErr
            return render_template("register.html", **self.context)

        # register user
        _password = generate_md5(password)
        user = User(name=user_name, password_hash=_password, email=email, sex=sex)
        db.session.add(user)
        commit()
        log.tag_info(WebLogTag.UserAccess, "Register Success, User: %s, email: %s, sex: %d" % (user.name, user.email, user.sex))

        self.user_login(user)
        self.context["errMsg"] = UserActionInfo.RegisterSuccess + user_name
        return render_template("register.html", **self.context)

    def login(self):
        """
        用户登录
        :return:
        """
        self.context["Check"] = ""
        if self.request.method == "GET":
            return render_template("login.html", **self.context)
        if self.request.method != "POST":
            raise ActionError(UserActionErr.RequestErr)
        par_dict = self.request.form.to_dict()
        user_name = par_dict["user_name"]
        password = par_dict['password']
        user = get_username(user_name)
        if not user:
            self.context["Check"] = UserActionErr.LoginErr
            return render_template("login.html", **self.context)

        if user.verity_password(password):
            self.user_login(user)
            self.context["Check"] = UserActionInfo.LoginSuccess + user_name
        return render_template("login.html", **self.context)

    @staticmethod
    def logout():
        """
        用户登出
        :return:
        """
        logout_user()
        flash("退出成功")
        return render_template("home.html")
