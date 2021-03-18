# IPC


## > 如何选择，以什么作为考量？



[Message Boundary issue](https://stackoverflow.com/questions/404604/comparing-unix-linux-ipc): 
> #### Message Boundary issue
> One determining factor when choosing one method over the other is the message boundary issue. You may expect "messages" to be discrete from each other, but it's not for byte streams like TCP or Pipe.

> Consider a pair of echo client and server. The client sends string, the server receives it and sends it right back. Suppose the client sends "Hello", "Hello", and "How about an answer?".

> With byte stream protocols, the server can receive as "Hell", "oHelloHow", and " about an answer?"; or more realistically "HelloHelloHow about an answer?". The server has no clue where the message boundary is.

> An age old trick is to limit the message length to CHAR_MAX or UINT_MAX and agree to send the message length first in char or uint. So, if you are at the receiving side, you have to read the message length first. This also implies that only one thread should be doing the message reading at a time.

> With discrete protocols like UDP or message queues, you don't have to worry about this issue, but programmatically byte streams are easier to deal with because they behave like files and stdin/out.
1. bytes stream: 抽象成 `file stream` or `stdin/stdout`（linux的核心概念）, 需要知道**消息长度**,在应用层进行解析
2. discrete protocols like **UDP** or **message queues**
    - 消息按包进行传输,不需要编码区分协议**边界**

Benchmark and Message Boundary: 
- **Pipe** I/O is the fastest but needs a **parent/child relationship** to work.
- Sysv IPC has a defined message boundary and can connect disparate processes locally, for example, **MQ**
- UNIX sockets can connect disparate processes **locally** and has **higher bandwidth** but no inherent message boundaries.
- TCP/IP sockets can connect any processes, even over the **network** but has **higher overhead** and no inherent message boundaries.


## > ipc分类
> Shared memory can be the most efficient since you build your own communication scheme on top of it, but it requires a lot of care and synchronization. Solutions are available for **distributing shared memory to other machines too**.(共享内存也可以跨机器)

> Sockets are the most portable these days, but require more overhead than pipes. The ability to transparently use sockets locally or over a network is a great bonus.

> Message queues and signals can be great for hard real-time applications, but they are not as flexible.

> These methods were naturally created for communication between processes, and using multiple threads within a process can complicate things -- especially with signals.


主要还是场景导向:
1. 是否需要明确的消息包边界?
    - 如果必须消息包则只能考虑 UDP 相关协议,以及消息队列
2. 是否需要满足不是父子进程的情况?
    - 如果有可能不是父子进程,则无法使用更快的pipe,而只能考虑fifo
3. 是否会有多线程的情况?
    - 典型的,信号不能在这里使用
4. 是否需要双向?全双工?
    - 管道可能淘汰
5. 是否需要一种广播的形势而不是一对一?
    - signal
    - 或者 socket - event driven?

### anonymous pipe: 
> 匿名意味着不对外开放，只在父子进程间传递消息
- usage: cat file | grep word
- 单向
- [implement](https://github.com/shaorui0/tiny_shell/blob/master/pipe_demo.c).
```c
#include <unistd.h>
int pipe(int pipefd[2]);
```
0. 底层通过内核 buffer 完成
    1. 读关，继续写导致 `SIGPIPE`
    2. 写关，读完 close
    3. 其他情况根据 buffer 确定是否被阻塞
1. 两个 fd 分别用来读写
2. 父子进程共享 fd
3. 父进程关闭 read_fd，子进程关闭 write_fd
4. 通信

TODO insert pic
[!pipe]()
![pipe process](./operator_system/process/ipc/fifo.png)


### named pipe (FIFO): 
> 典型用来解决匿名pipe的对外开放问题，但又带来了什么新问题？
![fifo](./operator_system/process/ipc/pipe_process.png)
- 半双工
- [some examples](http://beej.us/guide/bgipc/html/multi/fifos.html#fifonew)

### signal
- fork + signal
- [implement: tiny shell](https://github.com/shaorui0/tiny_shell)
### file lock
### Semaphores
- 某种同步原语，当需要锁功能或者生产消费一定数量的资源时
### socket
- 全双工，本机或网络
- TODO web server
- mmap
- [what is mmap?](https://github.com/shaorui0/fundamental_knowledge/tree/main/operator_system/memory/mmap)
    - mmap是什么？
    - 为什么需要mmap()
    - pros and cons
    - 一些可以运行的例子
### shared memory


### QA


#### socket 与 shared memory 在跨物理机执行时的对比
https://stackoverflow.com/questions/2101671/unix-domain-sockets-vs-shared-memory-mapped-file


1. Domain Sockets advantages
- blocking and non-blocking mode and switching between them
- you don't have to free them when tasks are completed

2. Domain sockets disadvantages
- must read and write in a linear fashion

3. Shared Memory advantages
- non-linear storage
- will never block
- multiple programs can access it

4. Shared Memory disadvantages
- need locking implementation
- need manual freeing, even if unused by any program

socket 的场景很常见,但是共享内存也有它的使用场景. 由于减少了数据复制,直接通过映射,如果是"读"更多的情况,使用共享内存会快一点(具体需要beachmark), 不然"同步"的开销可能降低使用共享内存所带来的内存提升.

#### shared memory 与 mmap 的区别

https://stackoverflow.com/questions/4836863/shared-memory-or-mmap-linux-c-c-ipc
https://stackoverflow.com/questions/21311080/linux-shared-memory-shmget-vs-mmap
https://linux.die.net/man/3/shm_open

出现的原因: 
- 和历史相关,unix 的版本问题,共享内存起始于 system V.

使用方式:
- [如果起始于多进程, mmap 直接有`MAP_ANONYMOUS` + `MAP_SHARED`模式用于共享] If you create your children via fork then mmap with MAP_ANONYMOUS | MAP_SHARED is by far the easiest way - just one call. MAP_ANONYMOUS is however a Linux extension not specified by POSIX.
- [如果起始于单进程, 通过结合使用, shm_open 创建共享内存**对象**, mmap映射这个对象]If you start the processes independently, but can supply them with a shared memory name then shm_open (+ ftruncate) + mmap with MAP_SHARED is two/three calls. Requires librt on some OSes.
- If your OS has /dev/shm/ then shm_open is equivalent to opening a file in /dev/shm/.

## reference
- [ref docs](http://beej.us/guide/bgipc/html/multi/index.html)
- [comparing-unix-linux-ipc](https://stackoverflow.com/questions/404604/comparing-unix-linux-ipc)
- https://stackoverflow.com/questions/4836863/shared-memory-or-mmap-linux-c-c-ipc
- https://stackoverflow.com/questions/21311080/linux-shared-memory-shmget-vs-mmap
- https://linux.die.net/man/3/shm_open
- https://zhuanlan.zhihu.com/p/94856678