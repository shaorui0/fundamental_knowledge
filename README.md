# fundamental knowledge


## OS

#### ipc

[valuable ref docs](http://beej.us/guide/bgipc/html/multi/index.html)

- anonymous pipe: 
    - usage: cat file | grep word
    - 单向
    - implement in Tiny Shell.
- named pipe: 
    - 双向，但是只能读or写
    - some examples: 
- signal
    - fork + signal
- file lock
- Semaphores
    - 某种同步原语，当需要锁功能或者生产消费一定数量的资源时
- socket
    - 全双工，本机或网络
- mmap/shared memory
    - [what is mmap?]()
        - mmap是什么？
        - 为什么需要mmap()
        - pros and cons
        - 一些可以运行的例子

