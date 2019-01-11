# [Kafka python doc](https://kafka-python.readthedocs.io/en/master/index.html)

## 准备工作

首先, 由于我们部署的kafka是需要kerberos认证的, 因此python连接kafka client需要认证.
- 安装: 
```bash
apt-get install libkrb5-dev
pip3 install gssapi
```

- 注意: 本项目需要以root权限运行(因为我用的kerberos配置都是用的root), 
如果是在windows下使用用pycharm的远程调试功能运行程序.则应进行以下配置:
    - 在虚拟机新建脚本python3_sudo.sh, 并赋予执行权限 sudo chmod a+x python3_sudo.sh
        ```bash
        #! /bin/bash 
        sudo python3 $*
        ```
    - 编辑visudo(!!!注意: 为了防止操作失误, 最好编辑前拍摄虚拟机快照)
        ```bash
        sudo visudo
        # 在最后一行输入
        %sudo ALL=NOPASSWD: /usr/bin/python3
        # 然后"ctrl+o", "enter", "ctrl+x"保存
        ```
    - 最后配置pycharm将Project Interpreter指向脚本

kafka-python 连接示例:
- 注意运行前一定要确保本地已经使用过kinit 认证过kafka.keytab
```python
from kafka import KafkaProducer

KafkaServer = ["192.168.1.89:9092", "192.168.1.89:9093", "192.168.1.89:9094"]

producer = KafkaProducer(
    bootstrap_servers=KafkaServer,
    api_version=(2, 11, 2),
    security_protocol="SASL_PLAINTEXT",
    sasl_mechanism='GSSAPI',
    sasl_kerberos_service_name='kafka',
)
```