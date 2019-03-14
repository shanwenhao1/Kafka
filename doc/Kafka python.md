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
    - 更改root密码(如果知道则可不执行次步骤):
        ```bash
        sudo passwd root
        ```
    - 设置ssh, 允许root远程连接
        ```bash
        # 编辑/etc/ssh/sshd_config, 添加
            PermitRootLogin yes
        # 重启ssh服务
        /etc/init_db.d/ssh restart
        ```
    - pycharm远程连接以root用户连接

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