from infra.flask.db import *
from infra.flask.app_init import db


def init_db():
    """
    创建所有表
    :return:
    """
    # TODO 数据库修改同步
    db.create_all()
    # db.dynamic_loader()
