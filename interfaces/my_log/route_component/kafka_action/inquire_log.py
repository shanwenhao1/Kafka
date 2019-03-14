#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/02/27
# @Author  : Wenhao Shan
import json
from flask import render_template
from flask_login import current_user
from infra import log
from infra.utils.error import ActionError
from infra.utils.time_utils import str_time_to_float
from infra.tool.enum.web_enum import WebLogTag, WebInfo, UserActionInfo, UserActionErr
from infra.flask.db.base_query import get_user
from infra.flask.db.models import RoleTopic, TopicInfo, TopicKey
from interfaces.my_log.route_component.kafka_action.action_status import LogReq
from domain.service.msg_service import inquire_msg, inquire_msg_time_limit

WEB_GROUP = "web group"


class KafkaLog:
    """
    Kafka web log handle class
    """

    def __init__(self, request):
        self.request = request
        self.context = dict()
        if not current_user.is_authenticated:
            log.tag_info(WebLogTag.UserAccess, UserActionInfo.SessionExpire)
            raise ActionError(UserActionInfo.SessionExpire)
        self.user = get_user(current_user.id)
        if self.user is None:
            log.tag_error(WebLogTag.UserAccess, "Web session error, couldn't get user(%s) "
                                                "when inquire log record" % str(current_user.id))
            raise ActionError(WebInfo.SessionErr)

    def inquire_topic(self):
        """
        inquire user topic
        :return:
        """
        if self.request.method != "GET":
            raise ActionError(UserActionErr.RequestErr)
            # inquire role topic
        self.context["topics"] = self.get_role_topic()
        return render_template("topic.html", **self.context)
        # if self.request.method != "POST":
        #     raise ActionError(UserActionErr.RequestErr)
        # # code=307 表示维持request type, code=303表示将post redirect to get
        # # https://stackoverflow.com/questions/15473626/make-a-post-request-while-redirecting-in-flask?r=SearchResults
        # # return redirect(url_for("my_log.record"), code=307)
        # return render_template("topic.html", **self.context)

    def inquire_record(self):
        """
        log handle
        :return:
        """
        # html post of submit request
        if self.request.method != "POST":
            raise ActionError(UserActionErr.RequestErr)
        data = self.request.form.to_dict()
        # ajax post request
        if "reqType" not in data.keys():
            data = self.request.get_json()

        data_keys = data.keys()
        if "reqType" not in data_keys or "topic" not in data_keys:
            raise ActionError(UserActionErr.ParamErr)
        req_type = str(data["reqType"])
        topic = data["topic"]
        topics = self.get_role_topic()
        msg_keys = self.get_msg_kye(topic)
        self.context["topics"] = topics
        self.context["currentTopic"] = topic
        self.context["msgKeys"] = msg_keys
        # if topic have no any message keys
        if len(msg_keys) == 0:
            self.context["currentMsgKey"] = ""
            self.context["filterTime"] = "" if "filterTime" not in data_keys else data["filterTime"]
            self.context["records"] = []
            return render_template("record.html", **self.context)

        # first inquire log of topic
        if req_type == LogReq.TopicReq:
            records = self.inquire_msg(topic, msg_keys[0])
            self.context["currentMsgKey"] = msg_keys[0]
            self.context["filterTime"] = ""
            self.context["records"] = records
            return render_template("record.html", **self.context)

        # then choice log inquire of topic
        if "currentMsgKey" not in data_keys or "filterTime" not in data_keys or "offset" not in data_keys:
            raise ActionError(UserActionErr.ParamErr)
        current_msg_key = data["currentMsgKey"] if data["currentMsgKey"] != "" else msg_keys[0]
        filter_time = data["filterTime"]
        offset = int(data["offset"])
        if req_type != LogReq.TopicKeyReq:
            raise ActionError(UserActionErr.ParamErr)
        records = self.inquire_msg(topic, current_msg_key, offset, filter_time)
        self.context["currentMsgKey"] = current_msg_key
        self.context["filterTime"] = filter_time
        self.context["records"] = records
        # return jsonify(self.context)
        return render_template("record.html", **self.context)

    def get_role_topic(self):
        """
        inquire current_user all topic name
        :return:
        """
        role_topic = RoleTopic.query.filter_by(role_id=self.user.id).all()
        topic_ids = [_topic.topic_id for _topic in role_topic]
        # inquire topic info
        topic_records = TopicInfo.query.filter(TopicInfo.topic_id.in_(topic_ids)).all()
        topics = [_record.topic_name for _record in topic_records]
        return topics

    @staticmethod
    def get_msg_kye(topic_name: str):
        """
        inquire all topic's msg_key according to topic_name
        :param topic_name:
        :return:
        """
        topic_info = TopicInfo.query.filter_by(topic_name=topic_name).first()
        if not topic_info:
            raise ActionError(WebInfo.TopicNotExist)
        topic_key = TopicKey.query.filter_by(topic_id=topic_info.topic_id).all()
        msg_keys = [_key.msg_key for _key in topic_key]
        return msg_keys

    @staticmethod
    def inquire_msg(topic: str, msg_key: str, offset: int = 0, filter_time: str = ""):
        """
        inquire msg(limit 20)
        :param topic:
        :param msg_key:
        :param offset:
        :param filter_time:
        :return:
        """
        if filter_time != "":
            filter_timestamp = int(str_time_to_float(filter_time, time_format="%Y-%m-%dT%H:%M:%S", need_ms=True))
            msgs = inquire_msg_time_limit(topic, WEB_GROUP, msg_key, offset=offset, timestamp=filter_timestamp)
        else:
            msgs = inquire_msg(topic, WEB_GROUP, msg_key, offset=offset)
        return msgs
