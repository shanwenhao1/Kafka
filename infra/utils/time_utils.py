#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/01/10
# @Author  : Wenhao Shan

import time
import datetime
import math
from dateutil import parser
from infra.utils.error import ActionError


def get_now_time(need_ms=False):
    """
    获取当前时间current time
    :param: need_ms bool 如果为True,则保留毫秒,否则毫秒置为0
    :return
    """
    if need_ms:
        return datetime.datetime.now()
    return datetime.datetime.now().replace(microsecond=0)


def get_now_time_timestamp(need_ms=False):
    """
    获取当前时间timestamp值
    :param need_ms: 为True时保留毫秒
    :return:
    """
    now_time = get_now_time(need_ms=True)
    if need_ms:
        timestamp = int(now_time.timestamp() * 1000)
    else:
        timestamp = int(now_time.timestamp())
    return timestamp


def get_int_time(last_time=0):
    """
    只给业务逻辑使用
    :param: last_time 用来获取相差的时间
    :return:
    """
    if not last_time:
        last_time = 0
    return int(time.time()) - last_time


def get_total_second(dt):
    """
    获取当前时间 减 过去时间（dt）的总秒数
    一般用于判断冷却时间是否到达
    :param dt:
    :return:
    """
    now_time = get_now_time()
    return (now_time - dt).total_seconds()


def is_pass_day(dt):
    """
    判断某个日期是否在今天之前
    :param dt:
    :return:
    """
    ct = get_now_time()
    if dt < ct.replace(hour=0, minute=0, second=0):
        return True
    return False


def time_str_to_timestamp(time_str):
    time_array = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    timestamp = int(time.mktime(time_array))
    return timestamp


def timestamp_to_datetime(timestamp):
    """
    时间戳转换为时间对象
    :param timestamp:
    :return:
    """
    return datetime.datetime.fromtimestamp(timestamp)


def datetime_to_str(input_time, time_format="%Y-%m-%d %H:%M:%S"):
    if not isinstance(input_time, datetime.datetime):
        raise TypeError
    if input_time is None:
        return None
    time_str = input_time.strftime(time_format)
    return time_str


def str_to_datetime(time_str, raise_error=False):
    """
    "2017-04-06 14:06:51" 字符串转日期时间对象
    :param time_str:
    :param raise_error:
    :return:
    """
    try:
        dt = parser.parse(time_str)
    except Exception as e:
        if raise_error:
            raise ActionError("时间字符串格式错误")
        else:
            raise e
    return dt


def get_another_time(dt, seconds=0, days=0, hours=0, minutes=0):
    """
    增加时间
    :param dt: datetime
    :param days: int 增加的天数
    :param hours: int 增加的小时
    :param minutes: int 增加的分钟数
    :param seconds: int 增加的秒数
    :return: datetime 增加后的时间
    """
    return dt + datetime.timedelta(days=days, seconds=seconds, hours=hours, minutes=minutes)


def get_different_day(dt, another_time=None):
    """
    获取相差的天数
    :param dt:
    :param another_time:
    :return:
    """
    another_time = get_now_time() if not another_time else another_time
    cst = another_time.replace(hour=-0, minute=0, second=0)
    cst_int_time = int(time.mktime(cst.timetuple()))
    dt_int_time = int(time.mktime(dt.timetuple()))
    dseconds = cst_int_time - dt_int_time
    if dseconds <= 0:
        # 都是当天的时间 直接返回0 表示不参与操作
        return 0
    else:
        days = float(dseconds) / float(60 * 60 * 24)
        if days <= 1:
            return 1
        else:
            return int(math.ceil(days))


def get_different_seconds(dt, str_time=False):
    if str_time:
        dt = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    cst = get_now_time()
    cst_int_time = int(time.mktime(cst.timetuple()))
    dt_int_time = int(time.mktime(dt.timetuple()))
    dseconds = cst_int_time - dt_int_time
    return dseconds


def datetime_to_timestamp(t):
    """datetime转化为时间戳"""
    time_str = datetime_to_str(t)
    return time_str_to_timestamp(time_str)


def get_rank_time(t=None):
    """
    根据时间得到一个(0, 1)的小数；
    时间越早，这个数值越大；
    一般用于榜单更新
    """
    if t is None:
        t = get_now_time()
    return 1 - datetime_to_timestamp(t) / 10000000000.0


def get_times(record_time, cd):
    """
    通过时间获取次数
    :return:
    """
    seconds = get_different_seconds(record_time)
    times = int(seconds / cd)
    return times


def get_date_start_time(today):
    """
    获取当天的最早时间
    :param today:
    :return:
    """
    return datetime.datetime.combine(today, datetime.time.min)


def get_date_end_time(today):
    """
    获取当天的最晚时间
    :param today:
    :return:
    """
    return datetime.datetime.combine(today, datetime.time.max)


def combine_date_and_hour(date, hour):
    return datetime.datetime.combine(date, datetime.time(hour))


def combine_date_and_time(date, combine_time):
    return datetime.datetime.combine(date, combine_time)


def str_time_to_float(str_time):
    """
    将str类型的时间转换为float型
    :param str_time:
    :return:
    """
    try:
        time_format = "%Y-%m-%d %H:%M:%S.%f"
        time_tuple = time.strptime(str_time, time_format)
        float_time = time.mktime(time_tuple)
    except:
        time_format = "%Y-%m-%d %H:%M:%S"
        time_tuple = time.strptime(str_time, time_format)
        float_time = time.mktime(time_tuple)
    return float_time


def float_time_to_str(float_time):
    """
    将float类型的时间转换为str类型
    :param float_time:
    :return:
    """
    if type(float_time) is not float:
        float_time = float(float_time)
    time_format = "%Y-%m-%d %H:%M:%S"
    date_time = datetime.datetime.fromtimestamp(float_time)
    str_time = datetime.datetime.strftime(date_time, time_format)
    return str_time


def get_yesterday():
    return get_another_time(get_now_time(), days=-1)


def _sleep(timeout):
    """
    自定义睡眠时间(不阻塞主线程)
    :param timeout:
    :return:
    """
    from threading import Event
    sleep = Event()
    sleep.wait(timeout=timeout)


if __name__ == '__main__':
    print(time_str_to_timestamp("2018-10-15 11:39:38"))
