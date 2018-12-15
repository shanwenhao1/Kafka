# Kafka Security

@TOC
- [中文文档](#中文文档)
    - [基于SASL/Kerberos认证](#基于SASL/Kerberos认证)
        - [创建Kafka kerberos principals](#创建Kafka kerberos principals)
        - [配置kafka节点 kerberos认证](#配置kafka kerberos节点认证)
    - [基于SSL的加密与认证](#基于SSL的加密与认证)

kafka的权限认证范围包含:
- Client与Broker之间: 使用SSL或者SASL
- Broker与Broker之间
- Broker与ZooKeeper之间


## 中文文档

[Doc](http://www.orchome.com/553)

### 基于SASL/Kerberos认证

[官方文档](http://kafka.apache.org/documentation/#security_sasl_kerberos))

#### 创建Kafka kerberos principals

- 创建kafka keytab(最好对Kafka每个节点都创建一个principle)
    ```bash
    addprinc -randkey kafka/192.168.1.89@EXAMPLE.COM
    ktadd -k /home/swh/Kerberos/kafka.keytab kafka/192.168.1.89@EXAMPLE.COM
    ```
- 将keytab文件拷贝至Kafka集群的每个节点上
    ```bash
    sudo scp kafka.keytab swh@192.168.1.89:/home/swh/Kafka/kafka_2.11-2.0.0
    ```

#### 配置kafka kerberos节点认证

- 配置Broker
    - 在config目录下创建kafka_server_jaas.conf, 其中Client是认证zookeeper的
        ```bash
            KafkaServer {
                    com.sun.security.auth.module.Krb5LoginModule required
                    useKeyTab=true
                    storeKey=true
                    keyTab="/home/swh/Kafka/kafka_2.11-2.0.0/kafka.keytab"
                    principal="kafka/192.168.1.89@EXAMPLE.COM";
            };
            Client {
                    com.sun.security.auth.module.Krb5LoginModule required
                    useKeyTab=true
                    storeKey=true
                    keyTab="/home/swh/Kafka/kafka_2.11-2.0.0/zkClient.keytab"
                    principal="zkClient@EXAMPLE.COM";
            };
        ```
    - 修改bin/kafka-server-start.sh, 添加jaas文件至启动参数, 使其可被broker找到
        ```bash
           # 或者不用if判断, 直接export
           if [ "x$KAFKA_OPTS"  ]; then
                export KAFKA_OPTS="-Djava.security.krb5.conf=/etc/krb5.conf -Djava.security.auth.login.config=/home/swh/Kafka/kafka_2.11-2.0.0/config/kafka_server_jaas.conf"
           fi
        ```
    - 修改Broker配置文件server.properties, 添加
        - 配置SASL端口和机制
            ```bash
            broker.id=0
            #advertised.host.name=192.168.1.89
            #advertised.listeners=SASL_PLAINTEXT://192.168.1.89:9092
            listeners=SASL_PLAINTEXT://:9092
            security.inter.broker.protocol=SASL_PLAINTEXT
            sasl.enabled.mechanisms=GSSAPI
            sasl.mechanism.inter.broker.protocol=GSSAPI
            # 配置服务器名称, 必须与kerberos的principal(kafka/192.168.1.89@EXAMPLE.COM)名称一致
            sasl.kerberos.service.name=kafka
            
            # 修改zookeeper连接设置
            zookeeper.connect=192.168.1.89:2181,192.168.1.89:2182,192.168.1.89:2183
            # Timeout in ms for connecting to zookeeper
            zookeeper.connection.timeout.ms=60000
            # 也可根据自己需求更改log.dir等
            ```
- 配置客户端
    - 修改producer.properties和consumer.properties
        ```bash
        # 集群
        bootstrap.servers=localhost:9092,localhost:9093,localhost:9094
        ecurity.protocol=SASL_PLAINTEXT
        sasl.mechanism=GSSAPI
        sasl.kerberos.service.name=kafka
        
        sasl.jaas.config=com.sun.security.auth.module.Krb5LoginModule required \
        useKeyTab=true \
        storeKey=true  \
        keyTab="/home/swh/Kafka/kafka_2.11-2.0.0/kafka.keytab" \
        principal="kafka/192.168.1.89@EXAMPLE.COM";

        
        # consumer group id
        group.id=test-consumer-group
        ```
    - 在conf目录下创建kafka_client_jass.conf, 客户端最好独立建一个kerberos 
    principal(这里偷懒直接使用了服务端的keytab)
        ```bash
            KafkaClient {
                    com.sun.security.auth.module.Krb5LoginModule required
                    useKeyTab=true
                    storeKey=true
                    keyTab="/home/swh/Kafka/kafka_2.11-2.0.0/kafka.keytab"
                    principal="kafka/192.168.1.89@EXAMPLE.COM";
            };
        ```


### 基于SSL的加密与认证

[Doc](http://kafka.apache.org/documentation/#security_ssl)


生成本地秘钥脚本, [keytool生成RSA证书](https://blog.csdn.net/freezingxu/article/details/71547485)
- Step1: 部署HTTPS, 为集群的每台机器生成秘钥(包含公私钥)和证书(用来识别机器). 
    - 参数意义:
        - keystore: 密钥仓库存储证书文件.密钥仓库文件包含证书的私钥(保证私钥的安全)
        - validity: 证书的有效时间(天)
    - 可运行以下命令验证生成的证书的内容
        ```bash
            keytool -list -v -keystore server.keystore.jks
        ```
    - 命令行
        - ![](picture/kafka%20ssl/1.png)
            ```bash
            > keytool -keystore server.keystore.jks -alias kafka-server -validity 365 -keyalg RSA -genkey
            ```
- Step2: 创建自己的client keystore和CA证书. 由于证书是未签名的, 
因此需要使用CA签名使得证书难以伪造, 提高安全性.
    - 生成的CA是一个简单的`公私钥对`和`证书`, 用于签名其他的证书.
    - 相反的是, 在step1中密钥库存储了每个机器自己的身份. 客户端的信任库存储所有客户端信任的证书, 
    将证书导入一个信任仓库也意味着信任由该证书签名的所有证书, 该特性称为`信任链`. (可由单个CA签名
    集群中的所有证书, 并且所有机器共享相同的信任仓库, 这样所有的机器可以验证其他的机器)
    - 命令行
        - 创建client keystore, ![](picture/kafka%20ssl/2.png)
            ```bash
            > keytool -keystore client.keystore.jks -alias kafka-client -validity 365 -keyalg RSA -genkey
            ```
        - 生成CA证书, ![](picture/kafka%20ssl/3.png)
            ```bash
            > openssl req -new -x509 -keyout ca.key -out ca.crt -days 365
            ```
- Step3: 签名证书, 用step2生成的CA来签名所有step1中生成的证书
    - 首先, 从密钥仓库中导出证书
        ```bash
        > keytool -keystore server.keystore.jks -alias localhost -certreq -file cert-file
        ```
    - 用CA签名
        ```bash
        > openssl x509 -req -CA ca-cert -CAkey ca-key -in cert-file -out cert-signed -days {validity} -CAcreateserial -passin pass:{ca-password}
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
    - 命令行
        - 将ca crt导入至server and client keystore, ![](picture/kafka%20ssl/4.png)
            ```bash
            > keytool -keystore server.trustkeystore.jks -alias CARoot -import -file ca.crt
            > keytool -keystore client.trustkeystore.jks -alias CARoot -import -file ca.crt
            ```
        - 导出cert文件, ![](picture/kafka%20ssl/5.png)
            ```bash
            > keytool -keystore server.keystore.jks -alias kafka-server -certreq -file kafka.server.crt
            > keytool -keystore client.keystore.jks -alias kafka-client -certreq -file kafka.client.crt
            ```
        - 使用ca cert do signed task, ![](picture/kafka%20ssl/6.png)
            ```bash
            > openssl x509 -req -CA ca.crt -CAkey ca.key -in kafka.server.crt -out kafka.server.signed.crt -days 365 -CAcreateserial
            > openssl x509 -req -CA ca.crt -CAkey ca.key -in kafka.client.crt -out kafka.client.signed.crt -days 365 -CAcreateserial
            ```
        - import the ca cert into server and client keystore., ![](picture/kafka%20ssl/7.png)
            ```bash
            > keytool -keystore server.keystore.jks -alias CARoot -import -file ca.crt
            > keytool -keystore client.keystore.jks -alias CARoot -import -file ca.crt
            ```
        - import the cert to server and client keystore after signed by CA cert, ![](picture/kafka%20ssl/8.png)
            ```bash
            > keytool -keystore server.keystore.jks -alias kafka-server -import -file kafka.server.signed.crt
            > keytool -keystore client.keystore.jks -alias kafka-client -import -file kafka.client.signed.crt
            ```
        - 拷贝jks(Java的keytools证书私钥文件)文件到集群的其他服务器上, (实际生产时的步骤)
            ```bash
            > scp yourDir/*.jks root@192.168.1.89:remoteDir/
            ```
        
- 以下为step1至step3的Kafkabash脚本, [具体步骤示例](ssl.md), [他人博客](https://blog.csdn.net/hwhanwan/article/details/82216016?utm_source=blogxgwz7):
    - 官方版本
        ```bash
            #!/bin/bash
            #Step 1:
            keytool -keystore server.keystore.jks -alias localhost -validity 365 -keyalg RSA -genkey
            #Step 2
            openssl req -new -x509 -keyout ca-key -out ca-cert -days 365
                   # 设置ssl.client.auth, 要求broker对客户端连接进行验证
                   # broker提供信任库及所有客户端签名了密钥的CA证书
            keytool -keystore server.truststore.jks -alias CARoot -import -file ca-cert
                    # 将生成的CA添加到client.truststore(客户的信任库), 以便client可以信任这个CA
            keytool -keystore client.truststore.jks -alias CARoot -import -file ca-cert
            #Step 3
            keytool -keystore server.keystore.jks -alias localhost -certreq -file cert-file
                    # 密码假设为123456
            openssl x509 -req -CA ca-cert -CAkey ca-key -in cert-file -out cert-signed -days 365 -CAcreateserial -passin pass:123456
            keytool -keystore server.keystore.jks -alias CARoot -import -file ca-cert
            keytool -keystore server.keystore.jks -alias localhost -import -file cert-signed
        ```
    - 完善版本
        ```bash
            #!/bin/bash
            # 生成server和client的非对称加密(RSA)的keystore
            keytool -keystore server.keystore.jks -alias kafka-server -validity 365 -keyalg RSA -genkey
            keytool -keystore client.keystore.jks -alias kafka-client -validity 365 -keyalg RSA -genkey
            # 生成CA证书, 有效期365天
            openssl req -new -x509 -keyout ca.key -out ca.crt -days 365
            
            keytool -keystore server.trustkeystore.jks -alias CARoot -import -file ca.crt
            keytool -keystore client.trustkeystore.jks -alias CARoot -import -file ca.crt
            
            keytool -keystore server.keystore.jks -alias kafka-server -certreq -file kafka.server.crt
            keytool -keystore client.keystore.jks -alias kafka-client -certreq -file kafka.client.crt
            
            openssl x509 -req -CA ca.crt -CAkey ca.key -in kafka.server.crt -out kafka.server.signed.crt -days 365 -CAcreateserial
            openssl x509 -req -CA ca.crt -CAkey ca.key -in kafka.client.crt -out kafka.client.signed.crt -days 365 -CAcreateserial
            
            keytool -keystore server.keystore.jks -alias CARoot -import -file ca.crt
            keytool -keystore client.keystore.jks -alias CARoot -import -file ca.crt
            
            keytool -keystore server.keystore.jks -alias kafka-server -import -file kafka.server.signed.crt
            keytool -keystore client.keystore.jks -alias kafka-client -import -file kafka.client.signed.crt
        ```
- Step4: 配置Kafka Broker
    - 更改server.properties(broker配置文件)
        ```bash
            listeners=PLAINTEXT://:9092,SSL://:9091
            # 启用SSL用于broker内部通讯(默认是PLAINTEXT):
            security.inter.broker.protocol=SSL
            ssl.keystore.location=/home/swh/Kafka/ssl/server.keystore.jks
            ssl.keystore.password=123456
            ssl.key.password=123456
            ssl.truststore.location=/home/swh/Kafka/ssl/server.trustkeystore.jks
            ssl.truststore.password=123456
            ssl.client.auth=required
        ```
    - 更改zookeeper.properties
        ```bash
            dataDir=/tmp/zookeeper
            clientPort=2181
            maxClientCnxns=0
            authProvider.1=org.apache.zookeeper.server.auth.SASLAuthenticationProvider
            requireClientAuthScheme=sasl
            jaasLoginRenew=3600000
        ```
    - 更改producer.properties
        ```bash
            security.protocol=SSL
            ssl.keystore.location=/home/swh/Kafka/ssl/client.keystore.jks
            ssl.keystore.password=123456
            ssl.key.password=123456
            ssl.truststore.location=/home/swh/Kafka/ssl/client.trustkeystore.jks
            ssl.truststore.password=123456
        ```
        
- Step5: 配置Kafka客户端, 更改.properties文件
    ```bash
        security.protocol=SSL
        ssl.keystore.location=/home/swh/Kafka/ssl/client.keystore.jks
        ssl.keystore.password=123456
        ssl.key.password=123456
        ssl.truststore.location=/home/swh/Kafka/ssl/client.trustkeystore.jks
        ssl.truststore.password=123456
    ```
