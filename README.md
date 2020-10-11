# fundamental knowledge


## OS

#### ipc

[valuable ref docs](http://beej.us/guide/bgipc/html/multi/index.html)

- anonymous pipe: 
    - usage: cat file | grep word
    - 单向
    - [implement](https://github.com/shaorui0/tiny_shell/blob/master/pipe_demo.c).
- named pipe: 
    - 双向，但是只能读or写
    - [some examples](http://beej.us/guide/bgipc/html/multi/fifos.html#fifonew)
- signal
    - fork + signal
    - [tiny shell](https://github.com/shaorui0/tiny_shell)
- file lock
- Semaphores
    - 某种同步原语，当需要锁功能或者生产消费一定数量的资源时
- socket
    - 全双工，本机或网络
    - TODO web server
- mmap
    - [what is mmap?](https://github.com/shaorui0/fundamental_knowledge/tree/main/operator_system/memory/mmap)
        - mmap是什么？
        - 为什么需要mmap()
        - pros and cons
        - 一些可以运行的例子

- shared memory