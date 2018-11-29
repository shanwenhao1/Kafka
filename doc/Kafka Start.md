# Kafka快速开始

## Quick Start

本教程假定你并没有Kafka或者ZooKeeper数据. 由于基于Unix和Windows平台的Kafka控制台脚本不同,
在windows上使用<font color=#ff99ff>bin\windows\\</font>而不是<font color=#ff99ff>bin/</font>,
并且要将脚本(script)后缀名改为.bat

#### <u>Step1: Download the code</u>

[下载](https://www.apache.org/dyn/closer.cgi?path=/kafka/2.0.0/kafka_2.11-2.0.0.tgz)2.0.0发行版并解压

```
> tar -xzf kafka_2.11-2.0.0.tgz
> cd kafka_2.11-2.0.0
```

#### <u>Step2: Start the server</u>

Kafka使用ZooKeeper, 所以你必须先启动一个ZooKeeper服务. 如果你没有的话, 你可以使用与Kafka打包的便利脚本
来获取一个ZooKeeper实例.

```
> bin/zookeeper-server-start.sh config/zookeeper.properties
[2013-04-22 15:01:37,495] INFO Reading configuration from: config/zookeeper.properties (org.apache.zookeeper.server.quorum.QuorumPeerConfig)
...

启动服务
> bin/kafka-server-start.sh config/server.properties
[2013-04-22 15:01:47,028] INFO Verifying properties (kafka.utils.VerifiableProperties)
[2013-04-22 15:01:47,051] INFO Property socket.send.buffer.bytes is overridden to 1048576 (kafka.utils.VerifiableProperties)
...
```

#### <u>Step3: Create a topic</u>