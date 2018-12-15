# Kafka SSl create

Kafka SSL 创建步骤及参数输入

- 1. 生成server keystore, ![](picture/kafka%20ssl/1.png):
    - 查看生成后的命令:
        ```bash
            keytool -list -keystore server.keystore.jks -v
        ```
- 2. 生成client keystore, ![]():