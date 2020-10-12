### 记录：
- `simple_anonymous_set_zero.c`里，`mmap`功能类似`malloc(5 int)` + `mmset(0)`



### 运行过程中出现错误的地方：
- 如果`read_from_fd.c`里面`MAP_PRIVATE`改为`MAP_SHARED`将导致`Mapping Failed`，而`ipc*.c`则能正确运行，想清楚这个flag的意义。


### 测试：

- 测试机器mmap限制
> 来源一个面试题：如果我调用malloc申请20GB内存，会发生什么？

不要着急回答，理清要点：
- **和什么因素有关？**
    - 字长，32bit限制进程地址空间（虚拟内存）4GB
    - malloc底层是怎么实现的？`strace`查看
        - sbrk
            OS如何进行内存管理的？底层怎么实现？
            - 维护一个链表连接可用内存块和不可用内存块（也方便整理碎片）
            - OS沿着链表找到复合用户需求的内存块
            - 切开，碎片插入之前的可用链表
            
            如果没有符合的内存块怎么办？
            - malloc请求延时，整理碎片
        - mmap(触发某个条件后)


    ```sh
    # 获取字长
    getconf LONG_BIT

    gcc -ggdb3 -O0 -std=c99 -Wall -Wextra -pedantic -o main.out test_mmap_limit.c
    ./main.out 0x40000000 # 4GB
    ./main.out 0x10000000000 # 1TiB
    ```