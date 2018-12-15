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