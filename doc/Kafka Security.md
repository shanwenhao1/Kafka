# Kafka Security

@TOC
- [中文文档](#中文文档)
    - [基于SSL的加密与认证](#基于SSL的加密与认证)
- [Kafka添加权限控制](#Kafka添加权限控制)

## [中文文档](http://www.orchome.com/170#/collapse-1033)

### [基于SSL的加密与认证](http://kafka.apache.org/documentation/#security_ssl)

生成本地秘钥脚本
- Step1: 部署HTTPS, 为集群的每台机器生成秘钥(包含公私钥)和证书(用来识别机器). 
    - 参数意义:
        - keystore: 密钥仓库存储证书文件.密钥仓库文件包含证书的私钥(保证私钥的安全)
        - validity: 证书的有效时间(天)
    - 可运行以下命令验证生成的证书的内容
        ```bash
            keytool -list -v -keystore server.keystore.jks
        ```
- Step2: 创建自己的CA. 由于证书是未签名的, 因此需要使用CA签名使得证书难以伪造, 提高安全性
    - 生成的CA是一个简单的`公私钥对`和`证书`, 用于签名其他的证书.
    - 相反的是, 在step1中密钥库存储了每个机器自己的身份. 客户端的信任库存储所有客户端信任的证书, 
    将证书导入一个信任仓库也意味着信任由该证书签名的所有证书, 该特性称为`信任链`. (可由单个CA签名
    集群中的所有证书, 并且所有机器共享相同的信任仓库, 这样所有的机器可以验证其他的机器)
- Step3: 签名证书, 用step2生成的CA来签名所有step1中生成的证书
    - 首先, 从密钥仓库中导出证书
        ```bash
            keytool -keystore server.keystore.jks -alias localhost -certreq -file cert-file
        ```
    - 用CA签名
        ```bash
            openssl x509 -req -CA ca-cert -CAkey ca-key -in cert-file -out cert-signed -days {validity} -CAcreateserial -passin pass:{ca-password}
        ```
    - 最后, 导入CA的证书和已签名的证书到密钥仓库
        ```bash
            keytool -keystore server.keystore.jks -alias CARoot -import -file ca-cert
            keytool -keystore server.keystore.jks -alias localhost -import -file cert-signed
        ```
        - keystore: 密钥仓库的位置
        - ca-cert: CA的证书
        - ca-key: CA的私钥
        - ca-password: CA的密码
        - cert-file: 出口, 服务器的未签名证书
        - cert-signed: 已签名的服务器证书
- step1至step3的bash脚本:
    ```bash
        #!/bin/bash
        #Step 1:
        keytool -keystore server.keystore.jks -alias localhost -validity 365 -genkey
        #Step 2
        openssl req -new -x509 -keyout ca-key -out ca-cert -days 365
               # 设置ssl.client.auth, 要求broker对客户端连接进行验证
               # broker提供信任库及所有客户端签名了密钥的CA证书
        keytool -keystore server.truststore.jks -alias CARoot -import -file ca-cert
                # 将生成的CA添加到client.truststore(客户的信任库), 以便client可以信任这个CA
        keytool -keystore client.truststore.jks -alias CARoot -import -file ca-cert
        #Step 3
        keytool -keystore server.keystore.jks -alias localhost -certreq -file cert-file
                # 密码假设为test1234
        openssl x509 -req -CA ca-cert -CAkey ca-key -in cert-file -out cert-signed -days 365 -CAcreateserial -passin pass:test1234
        keytool -keystore server.keystore.jks -alias CARoot -import -file ca-cert
        keytool -keystore server.keystore.jks -alias localhost -import -file cert-signed
    ```
- Step4: 配置Kafka Broker
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

### [基于SASL的认证](http://kafka.apache.org/documentation/#security_sasl)

Kafka使用Java的认证服务JAAS, 使用SASL配置.

#### JAAS configuration

##### 1. JAAS configuration for kafka brokers:

Client section被用来认证与zookeeper的SASL connection. 它允许brokers在zookeeper节点上
设置SASL ACL(lock zk 节点, 只有当前broker可以编辑). 如果你想使用处客户端之外的a section name
set the system property zookeeper.sasl.clientconfig to the appropriate name 
(e.g., -Dzookeeper.sasl.clientconfig=ZkClient).

ZooKeeper默认使用"zookeeper"作为service name, 如果你想修改, set the system property zookeeper.sasl.client.username to 
the appropriate name (e.g., -Dzookeeper.sasl.client.username=zk)

Brokers也可配置JAAS, 使用the broker configuration property `sal.jaas.config`. 前缀必须为




## Kafka添加权限控制

Kafka security 使用ssl加密传输数据(性能会大降)

kafka的权限认证范围包含:
- Client与Broker之间: 使用SSL或者SASL
- Broker与Broker之间
- Broker与ZooKeeper之间


添加权限的[步骤](http://kafka.apache.org/documentation/#security):
- 在Kafka Server服务器中, 在config目录中创建名为kafka_server_jaas.conf的文件
    ```bash
    KafkaServer{
        org.apache.kafka.common.security.plain.PlainLoginModule required
        # 该代理与集群其他代理初始化连接的用户名和密码
        username="kafka"
        password="kafkapswd"
        # 通过user_为前缀后接用户名方式创建连接代理的用户名和密码
        user_kafka="kafkapswd"
        # 示例: 创建用户名为mooc, 密码为moocpswd的连接代理
        user_mooc="moocpswd";
        };
    ```
- 在config目录中创建名为kafka_client_jaas.conf的文件
    ```bash
    KafkaClient {
        org.apache.kafka.common.security.plain.PlainLoginModule required
        username="mooc"
        password="moocpswd";
        };
    ```
- 修改启动的配置文件server.properties.(如果是集群则需要修改集群的broker对应的配置)
    ```bash
    listeners=SASL_PLAINTEXT://:9092        # if not localhost, you can use `listeners=SASL_PLAINTEXT://:xx.xx.xx.xx:9092`
    security.inter.broker.protocol=SASL_PLAINTEXT
    sasl.enabled.mechanisms=PLAIN
    sasl.mechanism.inter.broker.protocol=PLAIN
    ```
- 修改bin目录下的kafka-server-start.sh文件, 在文件中添加
    ```bash
    if [ "x$KAFKA_OPTS"  ]; then
        # config为你刚刚配置的ACL文件目录
        export KAFKA_OPTS="-Djava.security.auth.login.config=/usr/local/kafka_2.12-1.1.1/config/kafka_server_jaas.conf"
    fi
    ```
- 修改bin目录下的kafka-console-producer.sh和kafka-console-consumer.sh文件
    ```bash
    if [ "x$KAFKA_OPTS"  ]; then
        export KAFKA_OPTS="-Djava.security.auth.login.config=/usr/local/kafka_2.12-1.1.1/config/kafka_client_jaas.conf"
    fi
    ```