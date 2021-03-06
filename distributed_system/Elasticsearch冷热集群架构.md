# es的冷热数据处理

思考来源于一次面试，面试提出这样的问题。
实习期间只关注了DSL部分和一些es的基本概念，并未深入去了解其中集群扩展的东西。
经过提醒，发现，研究技术还是需要关注实质性的东西，对你用的东西要有“把握”。
先简单记录一下关于es集群扩展和冷热节点的知识，后面如果有使用到，再进行进一步的学习。

## 冷热数据索引特征

冷数据索引：查询频率低，基本无写入，一般为当天或最近2天以前的数据索引

热数据索引：查询频率高，写入压力大，一般为当天数据索引

## 为什么需要冷热节点？

cold、warm、hot spot 的概念并不是ES提出来的，分布式的概念中很早就有这一概念。

很明显，hot spot是经常读写的，相对的，cold spot 基本就属于“历史数据”一类。
典型的，由于ES的数据，是保存在内存中的（TODO）]
概念类似“局部性原理”
如何设置某些时间的数据为hot，这个时间节点的设置也很关键，直接影响性能。

当然，为了更好的缓解IO压力，分到多个节点效果更好。


众所周知，索引是为了更快的获取数据。但是创建索引的过程会比较 expensive。
如果数据量太大，而ES的数据又存在内存中，导致IO负载比较大。

W269N-WFGWX-YVC9B-4J6C9-T83GX

## ES的冷热架构部署

例子：比如电商数据极大。可以每个月建立一个索引，数据先写到热索引中，通过“工具”将3个月后的索引迁移到冷节点上面。

典型的，热节点机器使用“垂直扩展”，高性能机器。冷节点使用水平扩展，堆机器数。这样，就能保证最大化的性能

ES官方是建议使用SSD，但是成本


## 支持原理

第一：集群节点层面支持规划节点类型，这是划分热暖节点的前提。
第二：索引层面支持将数据路由到给定节点，这为数据写入冷、热节点做了保障。


## 参考

[Elasticsearch 冷热集群架构](https://www.cnblogs.com/caoweixiong/p/11988457.html)