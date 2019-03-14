#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/02/19
# @Author  : Wenhao Shan

from flask import request, render_template, Blueprint
from infra.flask.err_handle import web_err, action_err
from interfaces.my_log.route_component.user_action.session_action import UserAction
from interfaces.my_log.route_component.kafka_action.inquire_log import KafkaLog
from interfaces.my_log.route_component.kafka_action.msg_send import MsgHandle

# 关于static不起作用解决方法
# http://flask.pocoo.org/docs/0.12/blueprints/#static-files
kafka = Blueprint('my_log', __name__, template_folder="templates", static_folder="static")


@kafka.route('/', methods=['GET'])
@kafka.route('/home', methods=['GET'])
def home():
    return render_template('home.html')


@kafka.route('/register', methods=['GET', 'POST'])
@web_err
def register():
    return UserAction(request).register()


@kafka.route('/login', methods=['GET', 'POST'])
@web_err
def login():
    return UserAction(request).login()


@kafka.route('/logout', methods=['GET'])
def logout():
    return UserAction.logout()


@kafka.route('/topic', methods=['GET'])
@web_err
def topic():
    return KafkaLog(request).inquire_topic()


@kafka.route('/record', methods=['POST'])
@web_err
def record():
    return KafkaLog(request).inquire_record()


@kafka.route('/doc', methods=['GET', 'POST'])
def doc():
    return render_template('doc.html')


@kafka.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('test.html')


@kafka.route('/send', methods=['POST'])
@action_err
def send_msg():
    return MsgHandle(request).send_msg()
