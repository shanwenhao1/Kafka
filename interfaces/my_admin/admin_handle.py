#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/03/02
# @Author  : Wenhao Shan

import os
from flask import redirect, url_for, request, flash
from flask_admin.babel import gettext
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.view import log
from flask_admin.contrib.fileadmin import FileAdmin
from flask_login import current_user
from infra.utils.error import ActionError
from infra.flask.app_init import app, db
from infra.flask.db.models import User, TopicInfo, RoleTopic, TopicKey
from infra.flask.db.base_query import get_username
from domain.model.client_model.client_admin_model import ClientAdmin


class AdminModelView(ModelView):
    """
    Admin view, include authenticated
    """
    create_modal = True
    details_modal = True
    edit_modal = True

    def __init__(self, model, session, name=None, category=None, endpoint=None, url=None, static_folder=None,
                 menu_class_name=None, menu_icon_type=None, menu_icon_value=None):
        super(AdminModelView, self).__init__(model, session, name, category, endpoint, url,
                                             static_folder, menu_class_name, menu_icon_type,
                                             menu_icon_value)

    def is_accessible(self):
        """
        admin access handle
        :return:
        """
        _access = False
        if current_user.is_authenticated:
            # TODO 检测是否还存在获取不到name(调用__repr__只是为了解决__dict__获取不到的问题), 后续需解决
            current_user.__repr__()
            user = get_username(current_user.__dict__["name"])
            if user is not None:
                if user.is_admin:
                    _access = True
        return _access

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('my_log.login', next=request.url))

    # # a example of action use, but it's do nothing
    # @action('update',
    #         lazy_gettext('update'),
    #         lazy_gettext('Are you sure you want to update selected record?'))
    # def create(self, model):
    #     # do something update record here
    #     flash(lazy_gettext('Record was successfully update records were successfully update.'))


class AdminFile(FileAdmin):
    """
    Inherit FileAdmin, add access control
    """

    def __init__(self, base_path, *args, **kwargs):
        super(AdminFile, self).__init__(base_path, *args, **kwargs)

    def is_accessible(self):
        _access = False
        if current_user.is_authenticated:
            user = get_username(current_user.__dict__["name"])
            if user is not None:
                if user.is_admin:
                    _access = True
        return _access

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('my_log.login', next=request.url))


class UserAdminView(AdminModelView):
    """
    User Admin Model
    """
    # remove relation field from create action
    form_excluded_columns = ["role_topic"]

    def __init__(self,):
        super(UserAdminView, self).__init__(User, db.session)


class TopicAdminView(AdminModelView):
    """
    Topic Admin Model
    """
    # remove relation field from create action
    form_excluded_columns = ["role_topic", "topic_key"]

    def __init__(self,):
        super(TopicAdminView, self).__init__(TopicInfo, db.session)

    def create_model(self, form):
        """
        super create model and add create topic action
        :param form:
        :return:
        """
        try:
            model = self.model()
            form.populate_obj(model)
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
            # create topic
            with ClientAdmin() as client:
                client.create_topic(model.topic_name)
        except Exception or ActionError as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to create record. %(error)s', error=str(ex)), 'error')
                log.exception('Failed to create record.')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, True)

        return model

    def delete_model(self, model):
        """
        super delete model and add delete topic action
        :param model:
        :return:
        """
        try:
            self.on_model_delete(model)
            self.session.flush()
            self.session.delete(model)
            self.session.commit()
            # delete topic
            with ClientAdmin() as client:
                client.delete_topic(model.topic_name)
        except Exception or ActionError as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to delete record. %(error)s', error=str(ex)), 'error')
                log.exception('Failed to delete record.')

            self.session.rollback()

            return False
        else:
            self.after_model_delete(model)

        return True


# Admin 管理后台
admin = Admin(app, name="Kafka", template_mode="bootstrap3")
admin.add_view(UserAdminView())
admin.add_view(TopicAdminView())
admin.add_view(AdminModelView(RoleTopic, db.session))
admin.add_view(AdminModelView(TopicKey, db.session))

# 文件管理
path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "my_log/static")
admin.add_view(AdminFile(path, "/static", name="Static Files"))
