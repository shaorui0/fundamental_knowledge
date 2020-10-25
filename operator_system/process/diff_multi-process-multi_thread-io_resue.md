# 多线程、多进程、io复用


## 进程



#### pros

虽然现在的并发模型基本采用多线程和io复用的组合了，但是多进程也有其自己的优点：

1. 由于不『轻易』共享数据（[TODO 父子进程共享什么东西？](xxxxx)），race condition基本是很少出现的，也就是关于share resource相关的问题很少出现。比如典型的『并发计数竞争问题』。

#### cons

1. 开销：
    - 进程创建
    - 进程调度（上下文转换）

2. 数据共享：IPC
3. debug麻烦，一些工具比如`GDB`都不太好使用了

## io复用

#### pros

1. 【利好程序员】更好的控制。典型的场景，处理多个客户端的时候（event-drive）。（多进程并发模型需要每次close(listenfd)）TODO why？如果不close？test
2. 同一进程的缘故，共享数据更方便。

#### cons

1. 想要处理的事件（类型）越多，代码结构复杂
2. partial read问题（EOF），多进程信号处理很方便。
3. 【并发粒度】并发多少条指令（时间片）？(CSAPP)

## 多线程

#### pros

1. 开销比进程小
2. 多核上可以并行
3. 更好的共享信息（除了thread stack各自维护，其他segment都是共享的，包括：heap、read-only(const data), read-write(global/static), code, share memory(mmap, .so)）


#### cons

1. 由于共享的问题，潜在的并发问题都出现了：deadlock、race condition

## 总结

工业上比较好的方式：one loop(io reuse) per thread (muduo)