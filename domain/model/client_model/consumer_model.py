#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/11
# @Author  : Wenhao Shan

from kafka import KafkaConsumer
from kafka import TopicPartition, OffsetAndMetadata
from kafka.errors import IllegalStateError, UnsupportedVersionError, KafkaTimeoutError
from infra.conf.kafka_cfg import Config
from infra import log
from infra.utils.error import ActionError
from infra.tool.enum.kafka_enum import KafkaErr, KafkaInfo


class Consumer:
    """
    继承kafka-python KafkaConsumer, 封装自己的方法
    """

    def __init__(self, group_id: str = None):
        self.group_id = group_id

    def __enter__(self):
        self.cfg = Config().cfg
        self.consumer = KafkaConsumer(
            bootstrap_servers=self.cfg["serList"],
            # api_version=self.cfg["apiVersion"],
            api_version_auto_timeout_ms=self.cfg["autoVersionTimeout"],
            security_protocol=self.cfg["protocol"],
            sasl_mechanism=self.cfg["mechanism"],
            sasl_kerberos_service_name=self.cfg["kerverosSerName"],
            group_id=self.group_id,
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.consumer.close()

    def assign(self, partitions: list):
        """
        手动为当前consumer分配topic分区列表
        :param partitions: 手动分配分区[(topic, partition)]
        :return:
        """
        _partitions = [TopicPartition(_par[0], _par[1]) for _par in partitions]
        try:
            result = self.consumer.assign(_partitions)
        except IllegalStateError:
            log.tag_error(KafkaInfo.KafkaConsumer, "Manually consumer TopicPartitions error, "
                                                   "Topic Consumer is being in used")
            raise ActionError(KafkaErr.ConsumerInUsed)
        return result

    def assignment(self):
        """
        获取当前consumer分配的topic 分区:
        如果使用assign()手动分配, 则直接返回assign manage 配置
        如果使用subscribe()订阅的话则返回None(无订阅的情况) or set of topic partitions
        :return:
        """
        return self.consumer.assignment()

    def beginning_offsets(self, partitions: list):
        """
        获取指定partition最开始的offset, 该操作不影响当前partition offset
        :param partitions: 指定topic分区[(topic: partition)]
        :return:
        """
        _partitions = [TopicPartition(_par[0], _par[1]) for _par in partitions]
        try:
            result = self.consumer.beginning_offsets(_partitions)
        except UnsupportedVersionError or KafkaTimeoutError as e:
            if e.__class__ == UnsupportedVersionError:
                log.tag_error(KafkaInfo.KafkaConsumer, "API VERSION ERROR, DO NOT SUPPORT")
                raise ActionError(KafkaErr.NotSupport)
            else:
                log.tag_error(KafkaInfo.KafkaConsumer, "Get Beginning offset failed, Time out")
                raise ActionError(KafkaErr.GetOffsetFailed)
        return result

    def end_offsets(self, partitions: list):
        """
        获取指定partition结束的offset
        :param partitions: 指定topic分区[(topic: partition)]
        :return:
        """
        _partitions = [TopicPartition(_par[0], _par[1]) for _par in partitions]
        try:
            result = self.consumer.end_offsets(_partitions)
        except UnsupportedVersionError or KafkaTimeoutError as e:
            if e.__class__ == UnsupportedVersionError:
                log.tag_error(KafkaInfo.KafkaConsumer, "API VERSION ERROR, DO NOT SUPPORT")
                raise ActionError(KafkaErr.NotSupport)
            else:
                log.tag_error(KafkaInfo.KafkaConsumer, "Get end offset failed, Time out")
                raise ActionError(KafkaErr.GetOffsetFailed)
        return result

    def offsets_for_time(self, partitions_time: list, timestamp: int = -1):
        """
        寻找指定时间后的partition最早offset
        :param partitions_time: list of (topic, partition) if timestamp > 0, (topic, partition, timestamp) if timestamp = -1
        :param timestamp: 指定的开始查询时间, 如果是-1则表示每个partitions都有自己的时间配置
        :return:
        """
        if timestamp > 0:
            _partitions = {TopicPartition(_tuple[0], _tuple[1]): timestamp for _tuple in partitions_time}
        else:
            _partitions = {TopicPartition(_tuple[0], _tuple[1]): _tuple[2] for _tuple in partitions_time}
        try:
            result = self.consumer.offsets_for_times(_partitions)
        except UnsupportedVersionError or ValueError or KafkaTimeoutError as e:
            if e.__class__ == UnsupportedVersionError:
                log.tag_error(KafkaInfo.KafkaConsumer, "API VERSION ERROR, DO NOT SUPPORT")
                raise ActionError(KafkaErr.NotSupport)
            if e.__class__ == ValueError:
                log.tag_error(KafkaInfo.KafkaConsumer, "Value Error: Target Timestamp is negative")
            else:
                log.tag_error(KafkaInfo.KafkaConsumer, "Get offset by timestamp failed, Time out")
            raise ActionError(KafkaErr.GetOffsetFailed)
        return result

    def highwarter(self, topic: str, partition: int):
        """
        highwater offset 是分区中分配给下一个message produced的offset
        (一般用来与reported position做比较来计算滞后)
        :param topic:
        :param partition:
        :return:
        """
        result = self.consumer.highwater(TopicPartition(topic, partition))
        return result

    def commit(self, partition_offset: tuple, async_commit: bool = False):
        """
        提交偏移量至kafka, 阻塞直到成功或报错
        need group id not None
        :param partition_offset: (topic, partition, offset)
        :param async_commit: choose async commit
        :return:
        """
        topic = partition_offset[0]
        partition = partition_offset[1]
        _offset = partition_offset[2]
        offset = {
            TopicPartition(topic, partition): OffsetAndMetadata(_offset, None)
        }
        if not async_commit:
            self.consumer.commit(offset)
        else:
            self.consumer.commit_async(offset).add_errback(self.commit_err, topic=topic, partition=partition,
                                                           offset=_offset)

    def committed(self, topic: str, partition: int):
        """
        获取指定的topic partition最后一个committed offset, 配合commit使用
        :param topic:
        :param partition:
        :return:
        """
        _partition = TopicPartition(topic, partition)
        result = self.consumer.committed(_partition)
        return result

    def metrics(self):
        """
        获取consumer的性能记录(包含各个kafka broker)
        :return:
        """
        performance = self.consumer.metrics()
        return performance

    def partition_for_topic(self, topic_name: str):
        """
        查询指定topic的分区metadata
        :param topic_name:
        :return:
        """
        result = self.consumer.partitions_for_topic(topic_name)
        return result

    def available_partitions_for_topic(self, topic_name: str):
        """
        查询指定topic的可用分区
        :param topic_name:
        :return:
        """
        result = self.consumer.available_partitions_for_topic

    def pause(self, partitions: list):
        """
        挂起分区的请求(注意请求失败, 但可能有部分topic partition已经挂起)
        :param partitions: list of TopicPartition need pause, for example: [(topic1, partition1), (topic2, partition2)]
        :return:
        """
        _partitions = [TopicPartition(_par[0], _par[1]) for _par in partitions]
        try:
            self.consumer.pause(*_partitions)
        except:
            log.tag_error(KafkaInfo.KafkaConsumer, "Pause TopicPartition error, TopicPartition not exist")
            raise ActionError(KafkaErr.TopicPartitionNotExist)

    def get_paused(self):
        """
        获取当前被挂起的分区(用pause)
        :return:
        """
        return self.consumer.paused()

    def resume(self, partitions: list):
        """
        恢复pause挂起的分区
        :param partitions:
        :return:
        """
        _partitions = [TopicPartition(_par[0], _par[1]) for _par in partitions]
        self.consumer.resume(*_partitions)

    def seek(self, partition: tuple, offset: int):
        """
        修改TopicPartition的偏移量, 一般用于 poll
        :param partition: 指定的TopicPartition, (topic, partition)
        :param offset: 修改后的offset, >=0
        :return:
        """
        _partition = TopicPartition(partition[0], partition[1])
        self.consumer.seek(_partition, offset)

    def seek_many(self, partitions: list = None, is_begin: bool = True):
        """
        批量seek
        :param partitions: TopicPartition集合, [(topic, partition), ...], 当list为空时, 默认为已分配分区
        :param is_begin: True: 置位分区最初的可用offset, False: 置位end可用的offset
        :return:
        """
        if partitions is not None:
            _partitions = [TopicPartition(_par[0], _par[1]) for _par in partitions]
        else:
            _partitions = []
        if is_begin:
            self.consumer.seek_to_beginning(*_partitions)
        else:
            self.consumer.seek_to_end(*_partitions)

    def poll(self, timeout_ms=0, max_records=1000):
        """
        获取指定分区的Records, 会自动使用上一次的offset作为本次的开始, 也可用seek()手动指定
        当分区被pause挂起时, poll获取不到任何records
        :param timeout_ms:
        :param max_records:
        :return:
        """
        result = self.consumer.poll(timeout_ms, max_records)
        return result

    def position(self, partition: tuple):
        """
        获取指定分区next record的offset
        :param partition:
        :return:
        """
        _partition = TopicPartition(partition[0], partition[1])
        result = self.consumer.position(_partition)
        return result

    def subscribe(self, topic: list, pattern: str = None):
        """
        订阅一组topics
        :param topic: topic 列表
        :param pattern:
        :return:
        """
        try:
            self.consumer.subscribe(topic, pattern)
        except IllegalStateError or AssertionError or TypeError as e:
            if e.__class__ == IllegalStateError:
                log.tag_error(KafkaInfo.KafkaConsumer, "Subscribe topic error, %s" % e.__str__)
            log.tag_error(KafkaInfo.KafkaConsumer, "Subscribe topic error, Parameter Error")
            raise ActionError(KafkaErr.ParameterError)

    def unsubscribe(self):
        """
        取消订阅所有topic并清除分区配置
        :return:
        """
        self.consumer.unsubscribe()

    def subscription(self):
        """
        获取订阅状态
        :return:
        """
        result = self.consumer.subscription()
        return result

    def get_topics(self):
        """
        获取用户可见的topic
        :return:
        """
        result = self.consumer.topics()
        return result

    @staticmethod
    def commit_err(topic: str, partition: int, offset: int):
        """
        consumer commit offset failed callback function
        :param topic:
        :param partition:
        :param offset:
        :return:
        """
        log.tag_error(KafkaInfo.KafkaConsumer, "Kafka Consumer commit offset failed, "
                                               "{TopicPartition(%s, %s): %s}" % (topic, partition, offset))
        raise ActionError(KafkaErr.CommitOffsetFailed)

    @staticmethod
    def get_topic_partition(topic: str, partition: int):
        """
        获取TopicPartition, 这个方法是为了让外部不处理TopicPartition相关的
        :param topic:
        :param partition:
        :return:
        """
        return TopicPartition(topic, partition)
