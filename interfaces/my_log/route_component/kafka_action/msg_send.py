#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/03/08
# @Author  : Wenhao Shan

from flask import jsonify
from infra import log
from infra.utils.md5 import generate_md5
from infra.utils.error import ActionError
from infra.tool.enum.web_enum import UserActionErr
from infra.tool.enum.server_enum import ResponseStatus, ResponseMsg
from infra.flask.db.db_tool import db, commit
from infra.flask.db.models import TopicInfo, TopicKey, User, RoleTopic
from domain.service.msg_service import send_msg


def md5_check(secret_key: str, timestamp: float):
    """
    generate md5 according to timestamp and SecretKey
    :param secret_key:
    :param timestamp:
    :return:
    """
    return generate_md5(secret_key + str(timestamp))


class MsgHandle:
    """
    message send request handle
    """

    def __init__(self, request):
        self.request = request
        self.obj = self.request.get_json()
        if "verify" not in self.obj.keys() or "timestamp" not in self.obj.keys() or "username" not in self.obj.keys():
            raise ActionError(UserActionErr.ParamErr)
        self.role = User.query.filter_by(name=self.obj["username"]).first()
        if not self.role:
            raise ActionError(UserActionErr.UserNotExist)
        # verify action access
        if self.obj["verify"] != md5_check(self.role.md5_id, self.obj["timestamp"]):
            raise ActionError(UserActionErr.RequestErr)

    def send_msg(self):
        """
        send message
        :return:
        """
        if "topic" not in self.obj.keys() or "msgKey" not in self.obj.keys() or "msg" not in self.obj.keys():
            raise ActionError(UserActionErr.ParamErr)
        _topic = self.obj["topic"]
        _msg_key = self.obj["msgKey"]
        _msg = self.obj["msg"]
        topic_info = TopicInfo.query.filter_by(topic_name=_topic).first()
        if topic_info is None:
            raise ActionError(UserActionErr.TopicNotExist)
        # check topic is belongs to role or not
        role_topics = RoleTopic.query.filter_by(role_id=self.role.id).all()
        role_topic_ids = [_role_topic.topic_id for _role_topic in role_topics]
        if topic_info.topic_id not in role_topic_ids:
            raise ActionError(UserActionErr.TopicNotBelong)
        # TODO 考虑是否启用批量send message
        try:
            send_msg(_topic, _msg_key, _msg)
        except ActionError:
            raise ActionError(UserActionErr.ActionFailed)
        # check msgKey is record or not, if not record it
        topic_key = TopicKey.query.filter_by(msg_key=_msg_key).first()
        if topic_key is None:
            key = TopicKey(topic_id=topic_info.topic_id, msg_key=_msg_key)
            db.session.add(key)
            commit()
        res = {
            "errCode": ResponseStatus.Success,
            "errMsg": ResponseMsg[ResponseStatus.Success],
            "obj": {
            }
        }
        return jsonify(res)
