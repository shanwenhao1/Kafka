# Kafka

由于Kafka依赖于ZooKeeper服务, 因此在启动Kafka服务之前我们必须先启动ZooKeeper服务

Kafka是一个分布式的、可分区的、可复制的消息系统. 除了提供普通消息系统的功能之外, Kafka的设计特点有:
- Kafka将消息以topic为单位进行归纳
- 将向Kafka topic发布消息的程序称为producers
- 将预定topics并消费消息的程序称为consumer
- Kafka以集群的方式运行, 可以由一个或多个服务组成, 每个服务叫做一个broker.
- producers通过网络将消息发送到Kafka集群, 集群向消费者提供消息.

## [Kafka中文文档](doc/Kafka%20Note.md)

### [Kafka快速配置](doc/Kafka%20Start.md)

#### [Kafka Security模式下配置集群brokers](doc/Kafka%20Security.md)
- SSL认证模式, 暂时弃用
- SASL认证模式

### [Kafka Python](doc/Kafka%20python.md)

## 杂谈
- [Kafka深度好文](https://blog.csdn.net/lizhitao/article/details/39499283#commentBox)

## 部署时发现的问题

- kafka server.properties 中的log.dirs配置采用默认配置时, 在重启虚拟机的情况下会导致.log文件
被重写从而导致topic数据丢失
    - 问题发现:
    ```bash
    # 找到topic key数据存放的.log文件导出发现数据是存在的, .log文件大小也不为0. 重启后数据丢失
    sudo ./kafka-run-class.sh kafka.tools.DumpLogSegments --files /tmp/kafka/kafka-logs-0/test-2/00000000000000000000.log --print-data-log > 000000.txt
    ```
    ![](doc/picture/kafka%20issue/flush%20error.png)
    - 解决方案: 将log.dirs改为自定义目录