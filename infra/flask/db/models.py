#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/02/27
# @Author  : Wenhao Shan

from flask_login import UserMixin
from infra.flask.app_init import db
from infra.utils.uuid import new_uuid
from infra.utils.md5 import generate_md5
from infra.utils.time_utils import get_now_time


class User(UserMixin, db.Model):
    """
    用户model
    """
    __tablename__ = "role"
    id = db.Column(db.String(36), primary_key=True, default=new_uuid)
    name = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64))
    sex = db.Column(db.SmallInteger, default=0, doc="1 is male, 2 is female, default 0 unknown sex")
    md5_id = db.Column(db.String(36), default=new_uuid)
    is_admin = db.Column(db.Boolean, default=False)

    # create relationship with role_topic. it will delete all role_topic of role when delete role
    role_topic = db.relationship("RoleTopic", backref="role", lazy="dynamic", cascade="all, delete-orphan",
                                 passive_deletes=True)

    def verity_password(self, password: str):
        _password = generate_md5(password)
        return _password == self.password_hash

    # 相当于__str__方法
    def __repr__(self):
        return "User: %s %s %s %s" % (self.id, self.name, self.password_hash, self.email)


class TopicInfo(db.Model):
    """
    topic所属记录
    """
    __tablename__ = "topic"
    topic_id = db.Column(db.String(36), primary_key=True, default=new_uuid)
    topic_name = db.Column(db.String(64), unique=True)
    topic_info = db.Column(db.String(128), default="", doc="topic的描述")
    create_time = db.Column(db.DATETIME, default=get_now_time)

    # create relationship with role_topic. it will delete all role_topic of topic when delete topic
    role_topic = db.relationship("RoleTopic", backref="topic", lazy="dynamic", cascade="all, delete-orphan",
                                 passive_deletes=True)
    # relationship of topic and topic inquire key
    topic_key = db.relationship("TopicKey", backref="topic_key", lazy="dynamic", cascade="all, delete-orphan",
                                passive_deletes=True)

    # 相当于__str__方法
    def __repr__(self):
        return "Topic: %s %s %s" % (self.topic_id, self.topic_name, self.topic_info)


class RoleTopic(db.Model):
    """
    role所有的topic
    """
    __tablename__ = "role_topic"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.String(36), db.ForeignKey('role.id', ondelete='CASCADE'))
    topic_id = db.Column(db.String(36), db.ForeignKey("topic.topic_id", ondelete='CASCADE'))
    create_time = db.Column(db.DATETIME, default=get_now_time)

    __table_args__ = (
        db.UniqueConstraint("role_id", "topic_id", name="role_topic_id"),
        db.Index("role_topic_index", "role_id", "topic_id"),
    )


class TopicKey(db.Model):
    """
    topic下的key记录
    """
    __tablename__ = "topic_key"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic_id = db.Column(db.String(36), db.ForeignKey("topic.topic_id", ondelete="CASCADE"))
    msg_key = db.Column(db.String(36), index=True)

    __table_args__ = (
        db.UniqueConstraint("topic_id", "msg_key", name="topic_msg_key"),
        db.Index("topic_msg_key_index", "topic_id", "msg_key"),
    )
