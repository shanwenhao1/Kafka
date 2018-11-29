@[TOC]

# [Kafka Documentation](http://kafka.apache.org/documentation/)
[kafka博客](http://www.cnblogs.com/shijiaoyun/p/4860734.html?tvd=&from=timeline&isappinstalled=1)


[1.GETTING STARTED](#1-getting-started)
- [1.1 Introduction](#11-introduction)
- [1.2 Use Cases](#12-use-cases)
- [1.3 Quick Start](#13-quick-start)



## 1. GETTING STARTED

### 1.1 Introduction

- [Topics and Logs](#topics-and-logs)
- [Distribution](#distribution-分布式数据的分配)
- [Geo-Replication](#geo-replication)
- [Producers](#producers)
- [Consumers](#consumers)
- [Multi-tenancy](#multi-tenancy)
- [Guarantees](#guarantees)
- [Kafka as a Messaging System](#kafka-as-a-messaging-system)
- [Kafka as a Storage System](#kafka-as-a-storage-system)
- [Kafka for Stream Processing](#kafka-for-stream-processing)
- [Putting the Pieces Together](#putting-the-pieces-together-综上所述)


Kafka属于distributed streaming platform(分布式数据流平台)

一个分布式数据流平台有三种功能:
- 发布和订阅数据流, 类似于消息队列
- 以高容错的方式存储数据流(多分区主从备份, 涉及到负载均衡等)
- 及时的处理数据流

Kafka通常使用于两大类应用中:
- 搭建可以使数据在系统或应用之间流动的实时数据流管道(pipelines)
- 搭建可以针对流数据实行实时转换或作出相应反应的数据流应用

为了了解Kafka具体如何实现这些功能, 我们来从底层开始, 探索一下Kafka的功能.
首先讲几个概念:
- kafka作为一个集群运行在一个或多个服务器上
- kafka使用topics来分类储存数据流(streams of records)
- 每个数据流(record)都包含一个key、value、timestamp

Kafka有四个核心APIs:
- [Producer API](http://kafka.apache.org/documentation/#producerapi)负责生产数据流, 允许应用程序将记录流发布到一个或多个Kafka主题(topics)
- [Consumer API](http://kafka.apache.org/documentation/#consumerapi)负责使用数据流,允许应用程序订阅一个或多个主题并处理为其生成的数据流.
- [Streams API](http://kafka.apache.org/documentation/#streamsapi)负责处理或转化数据流,允许应用程序充当数据流处理器的角色, 处理来自一个或多个主题的
输入数据流,并产生输出数据流到一个或多个输出主题,以此来有效地将输入流转换成输出流.
- [Connector API](http://kafka.apache.org/documentation/#connectapi)负责将数据流与其他应用或系统结合,允许搭建和运行可重复使用的生产者或消费者,
将Kafka数据主题与现有应用程序或数据系统相连接的. 例如,关系数据库的连接器可能会将表的每个更改的事件,
都捕获为一个数据流.

![Kafka APIs](picture/kafka%20picture/kafka-apis.png)

Kafka的客户端和服务器之间的通信是用一种简单,高性能,语言独立的TCP协议实现的. 此协议是版本化的
并保持与旧版本的向后兼容性. 支持[很多语言的客户端](https://cwiki.apache.org/confluence/display/KAFKA/Clients).

#### Topics and Logs

作为Kafka对数据提供的核心抽象,我们先来深度探究一下主题(topic)这个概念

主题是发布的数据流的类别或名称. 主题在Kafka中,总是支持多订阅者的; 也就是说,主题可以有零个,一个或多个消费者订阅写到相应主题的数据.

对应每一个主题,Kafka集群会维护像一个如下这样的分区的日志:

![log anatomy](picture/kafka%20picture/log_anatomy.png)

每个分区都是是一个有序的,不可变的,并且不断被附加的记录序列,—也就是一个结构化提交日志(commit log).
为了保证唯一标性识分区中的每个数据记录,分区中的记录每个都会被分配一个一个叫做偏移(offset)顺序的ID号.

通过一个可配置的保留期,Kafka集群会保留所有被发布的数据,不管它们是不是已经被消费者处理.
例如,如果保留期设置为两天,则在发布记录后的两天内,数据都可以被消费,之后它将被丢弃以释放空间.
卡夫卡的性能是不会因为数据量大小而受影响的,因此长时间存储数据并不成问题.

![log consumer](picture/kafka%20picture/log_consumer.png)

事实上,在每个消费者上保留的唯一元数据是消费者在日志中的偏移位置.这个偏移由消费者控制:
通常消费者会在读取记录时线性地提高其偏移值(offset++),但实际上,由于偏移位置由消费者控制,
它可以以任何顺序来处理数据记录. 例如,消费者可以重置为较旧的偏移量以重新处理来自过去的数据,或者跳过之前的记录,
并从"现在"开始消费.

这种特征的组合意味着卡夫卡消费者非常轻量级 — 随意的开启和关闭并不会对其他的消费者有大的影响.
例如,您可以使用我们的命令行工具tail来查看任何主题的内容,而无需更改任何现有消费者所消耗的内容.

日志中的分区有几个目的. 首先,它保证日志的扩展性,主题的大小不受单个服务器大小的限制.
每个单独的分区大小必须小于托管它的服务器磁盘大小,但主题可能有很多分区,因此它可以处理任意数量的海量数据.
第二,它可以作为并行处理的单位 — 这个我们等下再多谈

#### Distribution-分布式数据的分配

在Kafka集群中,不同分区日志的分布在相应的不同的服务器节点上,每个服务器节点处理自己分区对应的数据和请求.
每个分区都会被复制备份到几个(可配置)服务器节点,以实现容错容灾.

分布在不同节点的同一个分区都会有一个服务器节点. 作为领导者("leader")和0个或者多个跟随者("followers").
分区的领导者会处理所有的读和写请求,而跟随者只会被动的复制领导者.如果leader挂了, 一个follower会自动变成leader.
每个服务器都会作为其一些分区的领导者,但同时也可能作为其他分分区的跟随者,Kafka以此来实现在集群内的负载平衡.

#### Geo-Replication

Kafka MirrorMaker为您的集群提供地异地备份支持.使用MirrorMaker,消息在多个数据中心或云区域上被复制.
您可以在主/从场景中使用此选项进行备份和恢复;或者在主动/主动场景中使用此选项来将数据放置得更靠近用户,
或者支持数据局部性需求.

#### Producers

生产者将数据发布到他们选择的主题. 生产者负责选择要吧数据分配给主题中哪个分区.这可以通过循环方式(round-robin)
简单地平衡负载,或者可以根据某些语义分区(例如基于数据中的某些关键字)来完成.我们等一下就来讨论分区的使用!

#### Consumers

消费者们使用消费群组名称来标注自己,几个消费者共享一个组群名,每一个发布到主题的数据会被传递到
每个消费者群组中的一个消费者实例. 消费者实例可以在不同的进程中或不同的机器上.

如果所有的消费者实例具有相同的消费者组, 则记录将在所有的消费者实例上有效地负载平衡,每个数据只发到了一个消费者

如果所有的消费者实例都有不同的消费者群体, 那么每个记录将被广播给所有的消费者进程,每个数据都发到了所有的消费者.

![consumer group](picture/kafka%20picture/consumer-groups.png)

如上图,一个两个服务器节点的Kafka集群, 托管着4个分区(P0-P3),分为两个消费者群. 消费者群A有2个消费者实例,消费者群B有4个.

然而,更常见的是,我们发现主题具有少量的消费者群,每个消费者群代表一个“逻辑订户”.每个组由许多消费者实例组成,
保证可扩展性和容错能力.这可以说是“发布-订阅”语义,但用户是一组消费者而不是单个进程.

在Kafka中实现消费的方式,是通过将日志中的分区均分到消费者实例上,以便每个实例在任何时间都是“相应大小的一块”
分区的唯一消费者.维护消费者组成员资格的过程,由卡夫卡协议动态处理. 如果新的实例加入组,
他们将从组中的其他成员接管一些分区; 如果一个实例消失,其分区将被分发到剩余的实例.

Kafka仅保证单个分区内的记录的有序性,而不保证单个主题中在多个分区之间的消息有序性. 每个分区排序结合按键分区,
足以满足大多数应用程序的需求. 但是,如果您需要保证主题中所有消息的有序性,则可以通过仅具有一个分区的主题来实现,
尽管这仅意味着每个消费者组只有一个消费者进程. Kafka多个分区的模式使得Kafka相对于传统的队列服务器支持了并发消费.
但注意consumer group的数量不能大于分区的数量.

#### Multi-tenancy

也可将Kafka部署为多租户方案, 通过配置来定义哪些用户可以访问和产生哪些topics, 或者限流. [详情, security documentation]()

#### Guarantees

在高可用的Kafka集群中,我们有如下的保证:
- 生产者发送到特定主题分区的消息将按照发送的顺序进行追加. 也就是说,如果记录M1由与记录M2相同的制造者发送,
并且首先发送M1,则M1将具有比M2更低的偏移并且在日志中较早出现.
- 消费者实例观察到数据的顺序,与它们存储在日志中的顺序一致.
- 对于具有复制因子N的主题,我们将容忍最多N-1个服务器故障,而不会丢失提交到日志的任何记录.

更多有关这些“保证”的细节会在有关设计的文档中.

#### Kafka as a Messaging System

Kafka的数据流概念与传统的企业消息系统相比如何？

消息系统传统上有两种模式: [队列]()和[发布-订阅](). 在队列中,消费者池可以从服务器读取,每条记录都转到其中一个;
在发布订阅中,记录将广播给所有消费者. 这两个模型中的每一个都有优点和缺点. 排队的优点是它允许您在多个消费者
实例上分配数据处理,从而可以扩展您的处理. 不幸的是,队列支持多用户,一旦一个进程读取数据就没有了.
发布订阅允许您将数据广播到多个进程,但无法缩放和扩容,因为每个消息都发送给每个订阅用户.

卡夫卡消费群体概念概括了这两个概念. 与队列一样,消费者组允许您通过一系列进程(消费者组的成员)来划分处理.
与发布订阅一样,Kafka允许您将消息广播到多个消费者组.

Kafka模型的优点是,每个主题都具有这两个属性,它可以进行缩放处理,也是多用户的, 没有必要选择一个而放弃另一个.

卡夫卡也比传统的消息系统有更强大的消息次序保证.

传统队列在服务器上保存顺序的记录,如果多个消费者从队列中消费,则服务器按照存储顺序输出记录. 然而,
虽然服务器按顺序输出记录,但是记录被异步传递给消费者,所以它们可能会在不同的消费者处按不确定的顺序到达.
这意味着在并行消耗的情况下,记录的排序丢失. 消息传递系统通常通过使“唯一消费者”的概念只能让一个进程从队列中消费,
但这当然意味着处理中没有并行性.

卡夫卡做得更好.通过分区,在一个主题之内的并行处理,Kafka能够在消费者流程池中,即提供排序保证,也负载平衡.
这是通过将主题中的分区分配给消费者组中的消费者来实现的,以便每一个分区由组中的一个消费者使用. 通过这样做,
我们确保消费者是该分区的唯一读者,并按顺序消耗数据. 由于有许多分区,这仍然平衡了许多消费者实例的负载.
但是请注意,消费者组中的消费者实例个数不能超过分区的个数.


#### Kafka as a Storage System

任何允许发布消息,解耦使用消息的消息队列,都在本质上充当传输中途消息的存储系统.
卡夫卡的不同之处在于它是一个很好的存储系统.

写入Kafka的数据写入磁盘并进行复制以进行容错. Kafka允许生产者等待写入完成的确认,这样在数据完全复制之前,写入是未完成的,
并且即使写入服务器失败,也保证持久写入.

Kafka的磁盘结构使用可以很好的扩容,无论您在服务器上是否有50KB或50TB的持久数据,Kafka都能保持稳定的性能.
由于对存储花费了很多精力,并允许客户端控制其读取位置,您可以将Kafka视为,专用于高性能,
低延迟的日志存储复制和传播的专用分布式文件系统.

#### Kafka for Stream Processing

仅读取,写入和存储数据流是不够的,Kafka的目的是实现流的实时处理.

在Kafka中,流处理器的定义是:任何从输入主题接收数据流,对此输入执行一些处理,并生成持续的数据流道输出主题的组件.

例如,零售应用程序可能会收到销售和出货的输入流,并输出根据该数据计算的重新排序和价格调整的输出流.

当然我们也可以直接用producer and consumer APIs在做简单的出列. 然而对于更复杂的转换,Kafka提供了一个
完全集成的Streams API.这允许我们构建应用程序进行更复杂的运算,或者聚合,或将流连接在一起.

该设施有助于解决这种类型的应用程序面临的困难问题:处理无序数据,重新处理输入作为代码更改,执行有状态计算等.

Stream API基于Kafka提供的核心原语构建:它使用生产者和消费者API进行输入,使用Kafka进行有状态存储,
并在流处理器实例之间使用相同的组机制来实现容错.

#### Putting the Pieces Together-综上所述

消息系统,数据存储和流处理的这种组合似乎是不寻常的,但是这些特性对于Kafka作为流媒体平台的角色至关重要.

像HDFS这样的分布式文件系统允许存储用于批处理的静态文件. 本质上,这样的系统允许存储和处理来自过去的历史数据.

传统的企业邮消息系统允许处理将在您订阅之后到达的未来消息. 以这种方式构建的应用程序在未来数据到达时及时处理.

Kafka结合了这两种功能,这种组合对于Kafka作为流应用程序和流数据管道平台来说至关重要.

通过组合存储和低延迟订阅,流式应用程序可以以相同的方式处理过去和未来的数据. 这是一个单一的应用程序可以处理历史记录数据,
而不是在到达最后一个记录时结束,它可以随着将来的数据到达而继续处理. 这是一个广泛的流处理概念,其中包含批处理以及
消息驱动应用程序.

同样,对于流数据流水线,订阅到实时事件的组合使得可以使用Kafka进行非常低延迟的管道传输; 可靠地存储数据的能力使得
可以将其用于必须保证数据传送的关键数据,或者与仅负载数据的离线系统集成,或者可能会长时间停机以进行维护. 流
处理设备可以在数据到达时转换数据.

### 1.2 Use Cases

- [Messaging](#messaging)
- [Website Activity Tracking](#website-activity-tracking)
- [Metrics](#metrics)
- [Log Aggregation(日志聚合)](#log-aggregation-日志聚合)
- [Stream Processing](#stream-processing)
- [Event Sourcing](#event-sourcing)
- [Commit Log](#commit-log)

本节描述了一些使用Apache Kafka的样例, 为了了解更全面的实际运用, 请阅读[该博客](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying)


#### Messaging

Kafka很好的取代了传统的消息代理. 应用消息代理的一系列原因有(从数据生产者中解耦, 缓存未处理消息等).
与大多数消息系统对比, Kafka具有更好的吞吐量、内置分区、复制和容错性, 这使得它成为大规模消息处理应用的
良好解决方案.

在我们的经验中, 消息传递的使用常常是较低的吞吐量、较高的响应速度(低延时), 最重要的是Kafka对长期稳定服务
的保证.

在此领域中, Kafka可以与传统的消息传递系统如[ActiveMQ](http://activemq.apache.org/)或[RabbitMQ](https://www.rabbitmq.com/)相媲美.

#### Website Activity Tracking

Kafka最初的用例是作为一个实时发布订阅源, 其能够重建用户活动跟踪流水线. 这意味着一些站点活动(页面视图、
搜索等用户操作)可以归类为一类活动类型发布到central topics.这些信号可以订阅一系列用例(如:
实时处理、实时监控以及加载Hadoop或离线数据仓库系统中进行离线处理和报告)

Activity Tracking通常作为一个高级卷包含多种活动信息, 为每个用户提供页面视图.

#### Metrics

Kafka通常用于运行监测数据, 这涉及到分布式应用统计数据的集中统计.

#### Log Aggregation-日志聚合

很多用户使用Kafka作为日志聚合的解决方案. 日志聚合通过从服务器收集物理日志文件, 并将它们
置入一个中心(a file server or HDFS perhaps)处理.Kafka抽象了文件的细节并将日志文件或事件数据的
抽象作为一个stream of messages.这满足了低延时处理、更容易地支持多个数据源和分部署数据流消费.

与Scribe或Flume等以日志为中心的系统相比,Kafka提供了同样良好的性能、更强的耐久性(备份)
以及端到端更低的延迟.

#### Stream Processing

Kafka大多数用户在由多个阶段组成的处理流(pipelines)中处理数据, 将kafka主题中的原始输入数据经过聚合、
填充、或者转换成新主题以进一步消耗或后续处理. 例如: 用于推荐新闻文章的处理管道可能从RSS提要中抓取
文章内容并将其发布到"文章"主题. 更进一步的处理可能是规范化和去重, 并发布为一个新的主题. 最后的处理
可能是将该文章推送给用户.

从0.10.0.0版本起, 一个更轻量级但却更强大的流处理库[Kafka Streams](http://kafka.apache.org/documentation/streams/)
可以用于上述处理中.除了Kafka Streams之外, 开源的流处理工具还有[Apache Storm](https://storm.apache.org/)和[Apache Samza](http://samza.apache.org/)


#### [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)

Event Sourcing是一种应用程序设计, 其中状态变化被记录在以时间顺序的记录序列中.Kafka对大存储日志
的支持使其能够完美的支撑该风格构建的应用.

#### Commit Log

Kafka可以作为分布式系统日志的外部提交. 日志有助于恢复节点数据, 并为故障节点同步恢复数据.
Kafka的[log compaction]()特性使其能够支持这种用法.类似于[Apache BookKeeper(记账本)]()
