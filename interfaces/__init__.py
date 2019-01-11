#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/10
# @Author  : Wenhao Shan
# Des      : DDD: interface 用户界面层 最顶层
# *	         负责向用户显示信息和解释用户命令
# *	         请求应用层以获取用户所需要展现的数据
# *	         发送命令给应用层要求其执行某个用户命令(某个业务逻辑, 比如转账)
# *	         用户界面层应该包含以下内容:
# *		     数据传输对象(Data Transfer Object): DTO也常被称作值对象(VO), 与领域层的VO不同的是DTO是数据传输
# *          的载体, 内部不应该存在任何业务逻辑, 通过DTO把内部的领域对象与外界隔离
# *		     装配(Assembler): 实现DTO与领域对象之间的相互转换, 数据交换, 因此Assembler几乎总是同DTO一起出现
# *		     表面, 门面(Facade): Facade的用意在于为远程客户端提供粗粒度的调用接口, 它的主要工作就是将一个用户请求
# * 	     委派给一个或多个service进行处理, 也就是我们常说的Controller。
