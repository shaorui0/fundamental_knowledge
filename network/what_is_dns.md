# DNS


## DNS属于哪一层？

应用层，但这个问题的本质是 TCP/IP 协议栈的四层的功能分别是什么？

### 应用层

允许访问OSI环境的手段（应用协议数据单元 APDU）


### 传输层

提供端到端的**可靠报文传递**和错误恢复（ 段Segment）	

### 网络层

负责数据包从**源到宿**的传递和**网际互连**（包 Packet）	

### 网络接口层

从网卡到对端机器的一个过程，比如MAC



## DNS是如何工作的？

client/browser <-> local DNS server <-> zone DNS server <-> global DNS server


## DNS use TCP or UDP?

第一阶段一般是使用UDP，这样保证效率，无需三次握手，典型的UDP适用场景。
第二阶段两个 server / database 之间的同步需要『可靠性』，这时适用TCP。
以及如果某个传输数据 > 512 bytes，将适用TCP。（为什么？涉及到UDP的特性）

## REFERENCE

- [REF: dns-works-on-tcp-and-udp](https://docs.microsoft.com/en-us/troubleshoot/windows-server/networking/dns-works-on-tcp-and-udp)

- [REF: when-do-dns-queries-use-tcp-instead-of-udp](https://serverfault.com/questions/404840/when-do-dns-queries-use-tcp-instead-of-udp)