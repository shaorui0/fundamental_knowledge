# 协程

tag: coroutine, subroutine, thread, concurrency, parallelism, generator, yield

## 异步编程模型的样子

1、最上层是进程；进程是**持有资源**的最小单位

2、中层是线程；线程不持有资源，是**CPU调度**的最小单位

3、下层是协程；协程既不持有资源、也不必在意CPU调度，它仅仅关注“协作式的、**自然的执行流程切换**”


## why

### 并发与并行

> Concurrency is the separation of tasks to provide interleaved execution. Parallelism is the simultaneous execution of multiple pieces of work in order to increase speed. —https://github.com/servo/servo/wiki/Design

[如何理解：程序、进程、线程、并发、并行、高并发？ - 大宽宽的回答 - 知乎](https://www.zhihu.com/question/307100151/answer/894486042)
- Concurrency is not Parallelism
- Concurrency enables parallelism & makes parallelism (and scaling and everything else) easy


### more light?

> First of all if coroutines run concurrently (never in parallel), why would anyone prefer them over threads? The answer is that coroutines can provide a very high level of concurrency with very little overhead. Generally in a threaded environment you have at most 30-50 threads before the amount of overhead wasted actually scheduling these threads (by the system scheduler) significantly cuts into the amount of time the threads actually do useful work.

在并发的问题上，由于线程的使用开销（创建开销（x KB - y MB）、调度开销（线程上下文））比较大，通常用户态的协程（开销与函数(subroutine)调用接近）就能解决问题。协程轻而易举的就能创建成千上万个。

### compare with THREAD

> Threads and coroutines are almost orthogonal features. Coroutines are about your programming model and threads are about your execution model.

协程与线程的区别有点像**并发与并行的区别**一样，不是一个维度的。多线程最终的目的（在现代操作系统、cpu多核的环境下）还是想并行执行提高效率。但是协程，完全是为了处理**并发**。一个是programming model，一个是execution model。

>  With threads, the operating system switches running threads preemptively according to its scheduler, which is an algorithm in the operating system kernel. With coroutines, the programmer and programming language determine when to switch coroutines; in other words, tasks are cooperatively multitasked by pausing and resuming functions at set points, typically (but not necessarily) within a single thread.

实际上许多线程的实现更像协程。

##### 线程：

- 抢占式的
- 内核调度
- 上下文转换expensive


##### 协程：

- **协作**式的，**完全由程序员指定**（也因为这一点，带来的巨大好处就是**基本不会在share resouce上出问题**，也就是不会出现**race condition**。你不可能自己设计一个有缺陷的并发代码结构吧 :)）
    > Because your routines now switch between each other a pre-determined points you can now also avoid locking on shared data structures (because you would never tell your code to switch to another coroutine in the middle of a critical section)
- 编程框架（程序员）调度
- 基本没有上下文转换，开销和函数调度差不多



### compare with subroutine

> Coroutines are a more generalized form of subroutines. Subroutines are entered at one point and exited at another point. Coroutines can be entered, exited, and resumed at many different points. They can be implemented with the async def statement.

回想函数/子程序调用，在线程栈里面会保留`return address`然后进行跳转执行。抽象出来，我们说子程序有一个entry pointer(and exit pointer)。协程在这方面则有多个re-entry pointer，是可以持续进入的（线性的）。

```py
# Yield 'remembers' where the co-routine is so when it is called again it will continue where it left off.

coroutine foo {
    yield 1;
    yield 2;
    yield 3;
}
print foo();
print foo();
print foo();
# Prints: 1 2 3

# Note: Coroutines may use a return, and behave just like a subroutine

coroutine foo {
    return 1;
    return 2; //Dead code
    return 3;
}
print foo();
print foo();
print foo();
# Prints: 1 1 1
```


#### why co-routines are receiving a lot of attention recently?

> And finally, co-routines are receiving a lot of attention because in some programming languages (such as Python) your threads cannot run in parallel anyway - they run concurrently just like coroutines, but without the low memory and free scheduling overhead.

关于python不能用线程：[TODO 臭名昭著的GIL]()



## when


典型的场景就是网络延迟等待了，cpu不愿意等的地方，协程当然也不愿意等。


> 从 CPU 的角度，协程其实更符合直觉。一个处理器核心本来就**没法同时处理两件事情**，要同时进行多件事情本来就需要正在运行的**让出处理器**，然后才能去处理另一件事情。只不过这个让出的过程是线程调度器**主动抢占**的。所以线程调度器是假定不同的线程是毫无关系的，所以它平均的分配时间片让处理器雨露均沾。
但是很快人们发现这不是事情的全部，很多时候两个线程不是完全独立的，他们会操作同一个资源。这个时候人们又发明了同步锁，使得一段时间内只有一个线程可以操作这个资源，其他线程只能等待。
然后我们很快发现，这特么不是**脱了裤子放屁**么？处理器本来同一时间就只能有一个线程在运行。是线程调度器抢断划分时间片给其他线程跑，现在其他线程又说特么我要等前面那个线程用完了这个资源才能运行。
也就是说，**在所有线程相互独立且不会阻塞的模式下，抢断式的线程调度器是不错的选择**。因为它可以保证所有的线程都可以被分到时间片不被程序员的垃圾代码所累。这对于某些事情来说是至关重要的，例如计时器、回调、IO触发器（譬如说处理请求）什么的。
但是在**线程不是相互独立，经常因为争抢而阻塞的情况下，抢断式的线程调度器**就显得脱了裤子放屁了，既然你们只能一个个的跑，那抢断还有什么意义？让你们**自己去让出时间片**就好了。再往后，大家发现经常有阻塞的情况下，主动让出时间片的协程模式比抢占式分配的效率要好，也简单得多。

结论：
- 任务之间相互独立时，使用抢占式的线程更好，这样同时保证不会有某个线程过多持有CPU
- 任务之间有依赖，经常**因为争抢而阻塞**的情况下，使用协程更好。本身就规定了一个一个跑（锁），那还不如用户主动出让CPU。

## how?


#####  协程写生产者消费者

可以看到，下面的代码，**解耦了生产者和消费者**，逻辑过程完全是**主动让出**的。
线程实现P/C问题，如果想解耦，需要有一个**阻塞队列**，由底层的条件变量对临界区进行空和满状态的控制（condition.wait/condition.signal）。

```
import time

def consumer():
    r = ''
    while True:
        n = yield r# 进行第二次迭代才重新回来
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        time.sleep(1)
        r = '200 OK'

def produce(c):
    c.next()
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n) # 这里的send也是根据yield来的
        print('[PRODUCER] Consumer return: %s' % r) # 这里只是一个返回结果
    c.close()

if __name__=='__main__':
    c = consumer()
    produce(c)



```



## 不是银弹

这个概念很早就出现了，那么它没有解决什么问题？
1. 它只是让并发实现更简单了，但是基本的设计（何时采用并发，如何保证不出bug？）还是需要用户去思考和设计。
2. **并行**这个维度上仍然需要配合进程来调度。

## 参考

- stackoverflow: what is coroutine?
- [出于什么样的原因，诞生了「协程」这一概念？](https://www.zhihu.com/question/50185085/answer/1342613525)
- [为什么编程语言对异步编程都是很晚近才开始支持的？](https://www.zhihu.com/question/389262477/answer/1566255353)