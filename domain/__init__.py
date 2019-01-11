#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/10
# @Author  : Wenhao Shan
# Des      : DDD: domain 领域层
# *	         领域层主要负责表达业务概念, 业务状态信息和业务规则
# *	         Domain层是整个系统的核心层, 几乎是全部业务逻辑都在该层实现
# *	         领域模型层主要包含以下内容:
# *		        实体(Entity): 具有唯一标识的对象
# *		        值对象(Value Objects): 无需唯一标识的对象
# *		        领域服务(Domain Service): 一些行为无法归类到实体对象或值对象上, 本质上是一些操作, 而非事物
# *		        聚合/聚合根(Aggregates/Aggregates Root): 聚合是指一组具有内聚关系的相关对象的集合, 每个聚合都有一个root和boundary
# *		        工厂(Factory): 创建复杂对象, 隐藏创建细节
# *		        仓储(Repository): 提供查找和持久化对象的方法(严格来讲Repository介于领域层和基础设施层之间,
# *		        它的存在让领域层感觉不到数据访问层的存在, 它提供一个类似集合的接口提供给领域层进行领域对象的访问)
