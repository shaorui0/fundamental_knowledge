# 协程

tag: coroutine, subroutine, thread, concurrency, parallelism, generator, yield

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



## how?

#####  yield例子，这个并不是典型的

> 计算量很大，但是不用全部等 ==> 迭代器（TODO python的迭代器）
python的yield，生成器，[TODO what is generator]()




#####  协程写生产者消费者（TODO）

```


```



## 不是银弹

这个概念很早就出现了，那么它没有解决什么问题？
1. 它只是让并发实现更简单了，但是基本的设计（何时采用并发，如何保证不出bug？）还是需要用户去思考和设计。
2. **并行**这个维度上仍然需要配合线程来调度。

