# Kafka快速开始

## Quick Start

本教程假定你并没有Kafka或者ZooKeeper数据. 由于基于Unix和Windows平台的Kafka控制台脚本不同,
在windows上使用<font color=#ff99ff>bin\windows\\</font>而不是<font color=#ff99ff>bin/</font>,
并且要将脚本(script)后缀名改为.bat

### <u>Step1: Download the code</u>

[下载](https://www.apache.org/dyn/closer.cgi?path=/kafka/2.0.0/kafka_2.11-2.0.0.tgz)2.0.0发行版并解压

```
> tar -xzf kafka_2.11-2.0.0.tgz
> cd kafka_2.11-2.0.0
```

### <u>Step2: Start the server</u>

- Kafka使用ZooKeeper, 所以你必须先启动一个ZooKeeper服务. 
    - 如果你没有的话, 你可以使用与Kafka打包的便利脚本来获取一个ZooKeeper实例.
        ```
        > bin/zookeeper-server-start.sh config/zookeeper.properties
        ...

- 在Zookeeper服务已经启动好以后, 使用以下命令启动服务(在server.properties内配置Zookeeper连接)
    ```
    > bin/kafka-server-start.sh config/server.properties
    ...

### <u>Step3: Create a topic</u>

- 创建一个topic
    ```bash
    # replication-factor代表每个分区在集群中复制的份数(要小于集群服务器数量)
    # partitions 表示创建主题的分区数量(分区越大, 性能越好)
    > bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
    ```
- 查看是否成功
    ```bash
    > bin/kafka-topics.sh --list --zookeeper localhost:2181
    # ACL模式
    > bin/kafka-topics.sh
    ```
    可以设置自动创建主题(当访问一个不存在的主题时)
    
### <u>Step4: Send some messages</u>

Kafka附带了一个命令行客户端, 该客户端将从文件或者标准输入获取输入, 并将其作为messages发送至Kafka集群.
默认情况下, 每一行将作为单独的消息发送.

run the producer并测试通过控制台发送一些消息至Kafka服务
```bash
> bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
# input some messages to test
```

### <u>Step5: Start a consumer</u>

相应的Kafka也有consumer的命令行讲消息转储到标准输出
```bash
> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
```

如果Step4 send messages与Step5 consumer在不同的终端运行的话, 你可以观察到send 输入一句话会立即显示
在consumer上.
    
### <u>Step6: Setting up a multi-broker cluster(建立多代理集群)</u>

- 首先, 每个broker都需要一个conf配置文件
    ```bash
    > cp config/server.properties config/server-1.properties
    > cp config/server.properties config/server-2.properties
    ```
- 其次, 编辑这些配置文件
    ```bash
    config/server-1.properties:
        broker.id=1                         # 唯一索引, 标志集群的单个节点
        listeners=PLAINTEXT://:9093         # 端口的话, 如果不在同一台机器上可不用更改使用默认端口9092
        log.dirs=/tmp/kafka/kafka-logs-1
        zookeeper.connect=localhost:2181,localhost:2182,localhost:2183  # 对应zookeeper集群
        zookeeper.connection.timeout.ms=60000                           # 原定超时时间为6000ms, 由于在单机上测试, 因此调大防止超时
 
    config/server-2.properties:
        broker.id=2
        listeners=PLAINTEXT://:9094
        log.dirs=/tmp/kafka/kafka-logs-2
        zookeeper.connect=localhost:2181,localhost:2182,localhost:2183
        zookeeper.connection.timeout.ms=60000
    ```
- 最后启动集群内的所有节点(如果要清除之前测试的数据, 直接删除掉对应的log目录就可以了)
    ```bash
    > bin/kafka-server-start.sh config/server-1.properties
    ```
    
    在这里我们使用supervisor进行管理, 启动成功后相应的data_log内会生成meta.properties文件存放相应的broker id.
    ```bash
    [program:Kafka1] ;
    user=root ; 进程运行的用户身份　　　　　
    directory=/home/swh/Kafka/kafka_2.11-2.0.0/bin ; 程序所在路径
    command=sudo ./kafka-server-start.sh  /home/swh/Kafka/kafka_2.11-2.0.0/config/server.properties ;
    stderr_logfile=/home/swh/Kafka/runlog/err.log ; 错误日志保存路径
    stdout_logfile=/home/swh/Kafka/runlog/kafka.log ; 输出日志保存路径
    stdout_logfile_maxbytes = 20MB
    stdout_logfile_backups = 3
    autostart=True
    autorestart=False
    startsecs=5 ; 启动时间5秒后无异常则表明成功启动
    startretries=0 ; 启动失败重启次数, 默认为3
    ```
    
    创建一个topic测试集群
    ```bash
    > bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 1 --topic my-replicated-topic
    ```
    
    使用以下命令来查看original topic所处位置
    ```bash
    > bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic my-replicated-topic
    ```
    
### <u>Step7: Use Kafka Connect to import/export data</u>

Kafka connect可作为导入导出数据的工具. 

以下范例通过Kafka connect可将data从文件导入至topic或者将data从topic导出至文件.
```bash
> bin/connect-standalone.sh config/connect-standalone.properties config/connect-file-source.properties config/connect-file-sink.properties
// 查看kafka topic connect-test的数据
> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic connect-test --from-beginning
```

### <u>Step8: Use Kafka Streams to process data</u>

`Kafka Streams` 是用于构建关键任务的实时应用程序和微服务的client library, 其输入和输出数据存储于Kafka集群中.
Kafka Streams在客户端中结合了编写简易性, java的标准部署以及Scala application. 这使得Kafka服务集群具有高度的可
伸缩性、弹性、容错性、分布式性等优点. [该例](http://kafka.apache.org/21/documentation/streams/quickstart)可以
帮助你快速入门.
