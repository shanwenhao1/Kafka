#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/03/04
# @Author  : Wenhao Shan

from infra import log
from infra.tool.enum.web_enum import WebLogTag, UserActionErr
from infra.flask.app_init import db
from infra.utils.error import ActionError


def commit():
    """
    db session commit, will rollback when error occurred
    :return:
    """
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        log.tag_error(WebLogTag.DbErr, "Db Session Committed Err: %s" % e.__str__())
        raise ActionError(UserActionErr.DataBaseErr)

