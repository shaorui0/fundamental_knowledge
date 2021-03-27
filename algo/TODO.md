# TODO
# design pattern
https://www.stackabuse.com/design-patterns-in-python/#:~:text=Design%20Patterns%20in%20Python%20Traditionally%2C%20design%20patterns%20have,but%20they%27re%20beyond%20the%20scope%20of%20this%20article.
https://www.stackabuse.com/creational-design-patterns-in-python/#singleton
https://python-patterns.guide/
https://refactoring.guru/design-patterns/python


# memset

# memcpy
https://aticleworld.com/how-to-use-memcpy-and-how-to-write-your-own-memcpy/
https://www.tutorialspoint.com/write-your-own-memcpy-in-c
https://www.geeksforgeeks.org/write-memcpy/
https://www.embhack.com/memcpy-and-memmove/
https://stackoverflow.com/questions/17498743/how-does-the-internal-implementation-of-memcpy-work
http://www.danielvik.com/2010/02/fast-memcpy-in-c.html

---

1. 昨天学的几个topic，做几个相关的题目看看


    - 树上DFS
    - merge k list
    - 动态规划
        - 01背包
2. python 怎么用栈？

整理一下面试相关题目：
0. 刷题
    - 动态规划，背包
    - 字符串匹配
    - 昨天的写的 +-*/的编译器（这个写出来有很多corner case）
1. DB
    - 看看区别什么的
    - 还好之前都generate了，不然丢失了很多信息
2. redis
3. 网络
4. 回顾一下 OS 的东西，能不能连成串？
    - 有很多相关的问题，我觉得都可以连成串。典型的进程管理、内存管理

---

# 题外话，分布式
其实如果问什么分布式，我完全可以说说我知道的东西、
比如什么是分布式，他的本质是什么？（之前在知乎看到的那些东西）

关于MQ，赶快写一篇文章自己理解一下

算法是一方面，关键还是面试过程中体现自己的思维过程。

关于分布式的问题，完全可以看看那个 ddia ，的四个章节，对整体有一个把握

比如，我觉得分布式得本质就是，一些跨机器的进程通信
然后肯定是有一些个节点，这些节点各自有一些自己的角色
然后我会说，会有几种节点组成，各自是个什么样场景，为什么这么设计。。。这些书上都有，完全能解答一些困惑


同时，你最好，对整本书，看过的书进行一些总结，这样的话，真的很能在面试上加分呐


比如说，他让你说索引，你再说一句，其实我觉得还有一种nosql中的索引也有必要提一下，然后关于这种索引与B树的一个对比，

然后我会说，这东西是从哪本书上看来的，很有启发。

然后说一下这本书对我个人的影响？对我做东西有什么影响？我能串起来吗？

然后我会说一说，是否遇到过性能调优的问题，？必然有很多count？然后我会想某张表会指定引擎吗？我可以换一种引擎吗？

---

1. 我现在其实很应该看看怎么对一个网站进行加压？应该关注哪些指标？
---
explain sql


1. 怎么能命中索引？
    - 看你where 什么？
    - 看你覆盖索引
---

最基本的几个题目，一定要先写会
1. 公共父节点
2. 水平迭代处理
3. 平面内最短路径，比较难，不过思路可以说一下
4. 逆序对
5. 转置矩阵，矩阵旋转
6. 链表问题，连续k个数的众数
7. 树的前中后序遍历，非递归
    - 另：递归的一些扩展
8. 递归的优化，尾递归
写出代码来，然后跑跑看

代码写完了，骑个车去那儿看看书，典型的tcp的问题，以及一些对比，最好能给出适当的场景，比如什么视频播放、腾讯会议的视频实时传输
qq 发送是通过什么？我觉得是通过tcp 吧，不能老丢包，

场景

---
关于找工作

1. 什么是雇主看重的？
2. 我应该做哪些努力能够最大程度的去展示自己的所学？


1. blog + github + 自己经常浏览的网站？

## blog 对行业的理解，对知识的掌握情况




## reference

1. 邹欣，现代软件工程
    - 邹欣的blog，他教同学们怎么进行软件工程的学习
2. 刘伟鹏
    - blog，他讲述怎么进行学习
3. medium
    - 这个被墙了，

---



## 必须了解的MySQL三大日志：binlog、redo log和undo log
https://zhuanlan.zhihu.com/p/190886874


## mysql主从复制，半同步，主主复制架构的实现
https://developer.aliyun.com/article/484023
https://yq.aliyun.com/articles/481964?spm=a2c4e.11153940.0.0.70c54bdbqongX4
https://yq.aliyun.com/articles/491454
https://blog.csdn.net/u010353408/article/details/77964157
https://stackoverflow.com/questions/66764012/understanding-mysql-innodb-replication-issue
https://stackoverflow.com/questions/3402794/mysql-replication

---

# 面向简历工作

1. 其实面试过几次就知道，简历应该怎么写，面试官关注什么东西


# 表现出来的可培养性

工程师
什么算一个好的工程师
我觉得本质算一个设计者而不是单纯的实现别人构想的东西
从更高的层次去看问题

明天大概就是看代码了，具体要看什么东西，典型的就是搞清楚代码的大致结构，但是业务功能啥的估计都是整合在一起的，可能在同一个文件不同的函数表达上。
一定要主要我需要学习的点。

go的实践，我也可以开始学学了。其实没什么大的东西，典型的就是一些初始化，一些循环。。。
---

# 
https://www.cnblogs.com/xudong-bupt/p/3433643.html
https://stackoverflow.com/questions/25338862/why-time-wait-state-need-to-be-2msl-long
https://stackoverflow.com/questions/40417087/how-if-the-last-ack-is-lost-in-tcp-termination


https://docs.paloaltonetworks.com/pan-os/8-1/pan-os-admin/networking/session-settings-and-timeouts/tcp/tcp-half-closed-and-tcp-time-wait-timers

# singleton
https://refactoring.guru/design-patterns/singleton/cpp/example#:~:text=Singleton%20in%20C++%20Singleton%20is%20a%20creational%20design,super-handy,%20they%20break%20the%20modularity%20of%20your%20code.
https://github.com/shaorui0/recipes-1/blob/master/thread/Singleton.h
https://www.cnblogs.com/xudong-bupt/p/3433643.html

---
# ETL

1. 背景
2. 解决的问题


面试官经常会质疑我框架写的太简单，没有考虑多机部署的问题
我的数据任务都有一些什么样的？
我感觉我们主要是处理一些离线数据
典型的会有一些广告主的数据过来，然后。。。我会判断他们的数据状态，判断是否发人审啥的
单机的数据量不大，没有涉及到多机
我是这样觉得的
未来我可以把它封装成任务，像我们celery队列这样，做成一个离线任务

但由于主要的功能都是shellProcess提供的，基本很多都是本机处理
有一些线上的东西，不涉及到拉取到本机的，我感觉可以作一个xxx通过队列进行发送
任务封装成消息
但是这就没有Airflow的用处了
是多机的吗？调度系统
A
问单机还是多机，本质是 Airflow 的高可用，稍微研究一下这个框架的高可用部分？

现在的问题就是Airflow集群架构是什么样的？
celery的集群架构是怎么样的
然后ATQ的集群架构是怎么样的

可以说一些airflow/celery 的多级扩展能力