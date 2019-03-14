# 我的kafka日志聚合说明文档

## 用前须知

- 使用前先注册账户, 如果已有账户则需登录
- 请确认当前账户拥有足够的访问权限(相关topic的访问权限), 如果没有请联系管理员申请topic
- 使用前, 如有兴趣可了解kafka帮助你更加熟练使用, [官方文档](http://kafka.apache.org/documentation.html)

## kafka使用说明

本项目作为我的科技的日志聚合系统, 目标是提供一个方便的快捷的跨系统日志收集及查询服务.
但不考虑永久保留, 目前暂定日志保留7天. 如需保留更长周期, 请联系管理员进行配置

### 生产数据
kafka操作时按照topic进行操作的, 本日志聚合使用topic下的message key作为消息生成和消费的划分. 
因此用户如有需求, 可自定义不通类型消息的message key(请慎重考虑, 关乎查询效率).

请求地址: /my_log/send

请求格式:
```python
{
    "username": "test",             # str类型, 消息所属的用户名
    "verify": "md5",                # str类型, md5_id + timestamp生成的md5值, md5_id请向管理员提供用户名并索要
    "timestamp": 199992222,         # float类型, 当前时间戳
    "topic": "test",                # str类型, 消息所属的topic
    "msgKey": "test_key",           # str类型, 消息类型
    "msg": "test send message",     # str类型, 消息具体信息
}
```

返回格式:
```python
{
    "errCode": 0,                   # int类型, 请求是否成功 0: 成功, 1: 失败
    "errMsg": "",                   # str类型, 错误信息
    "obj": {},                      # json类型, 其他信息
}
```

### 使用网站查询日志

1. 点击主页中的`日志记录`, ![](picture/web%20use/1.png)
2. 选择一个topic进行查询, 此时的消息是默认该topic所属的第一个message key. 后续可自由选择.
![](picture/web%20use/2.png)
3. 查询的消息如下图所示, 鼠标继续往下拉去会查询当前页面最早一条消息之前的消息![](picture/web%20use/3.png)
    - 注意: 最顶上的一行是筛选条件, 分别为选择topic, 选择message key, 和查询某个时间点之前的消息
    (该时间点之后的消息都会过滤掉)

## 负责人

负责人: 单文浩  联系方式: 761542858(QQ)