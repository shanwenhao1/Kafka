#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/02/27
# @Author  : Wenhao Shan

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask("Kafka")

# database connection
# url的格式为：数据库的协议：//用户名：密码@ip地址：端口号（默认可以不写）/数据库名
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@192.168.1.89:3306/kw_kafka"
# 这个配置将来会被禁用,设置为True或者False可以解除警告信息,建议设置False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your own secret key"
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
# 创建数据库操作对象
db = SQLAlchemy(app)
