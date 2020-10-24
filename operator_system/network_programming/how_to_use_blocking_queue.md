# 阻塞队列


## 场景

本质：作为任务存放的容器。

多线程的环境下，一个任务过来，不是立即执行的。一个路由thread进行分发，一些worker thread来取。那worker从哪里取呢？典型的就是『先进先出』的队列。

一个典型的过程：
```
1. 任务过来
2. 分发线程将任务存到queue中
3. 如果有线程闲置，就会去取
    3.1. queue会将task传递给线程
    3.2. queue会同时将task pop掉（4、5过程原子性）
```

但是这个队列既然是在并发环境，就得防止**竞争**，哪个环节会出现竞争？『存』、『取』操作。
- 存，可能多个任务同时存放，导致抢占queue，需要对queue进行加锁。
- 取，多个线程同时取task，这就需要对queue进行加锁，每次只能让单个线程进来


## how to use


#### 单个线程

```py
"""
The queue module implements multi-producer, multi-consumer queues. It is especially useful in threaded programming when information must be exchanged safely between multiple threads. The Queue class in this module implements all the required locking semantics.
"""
import threading, queue
import time
q = queue.Queue()

def worker():
    while True:
        item = q.get()
        print(f'Working on {item}')
        print(f'Finished {item}')
        time.sleep(0.5)
        q.task_done()

# turn-on the worker thread
threading.Thread(target=worker, daemon=True).start()

# send thirty task requests to the worker
for item in range(30):
    q.put(item)
print('All task requests sent\n', end='')

# block until all tasks are done
q.join()
print('All work completed')

```

#### 多线程配合队列

```py
import queue 
import threading 
import time 

thread_exit_Flag = 0

class sample_Thread (threading.Thread): 
    def __init__(self, threadID, name, q): 
        threading.Thread.__init__(self) 
        self.threadID = threadID 
        self.name = name 
        self.q = q 
    def run(self): 
        print ("initializing " + self.name) 
        process_data(self.name, self.q) 
        print ("Exiting " + self.name) 

# helper function to process data
def process_data(threadName, q): 
    while not thread_exit_Flag: # 如果有任务，就一直获取任务
        queueLock.acquire() 
        if not workQueue.empty(): 
            data = q.get_nowait() 
            queueLock.release() 
            print ("% s processing % s" % (threadName, data)) 
            workQueue.task_done() # 如果要使用queue.join，就必须每次标记task_done
        else: 
            queueLock.release() 
            time.sleep(1) 
  
thread_list = ["Thread-1", "Thread-2", "Thread-3"] 
name_list = ["A", "B", "C", "D", "E"] 
queueLock = threading.Lock() 
workQueue = queue.Queue(10) 
threads = [] 
threadID = 1
  
# Create new threads 
for thread_name in thread_list: 
    thread = sample_Thread(threadID, thread_name, workQueue) 
    thread.start() 
    threads.append(thread) 
    threadID += 1
  
# Fill the queue 
queueLock.acquire() 
for items in name_list: 
    workQueue.put(items) 
  
queueLock.release() 
  
# Wait for the queue to empty 
workQueue.join() # 需要在每个任务完成的时候加上task_done

# Notify threads it's time to exit 
thread_exit_Flag = 1

# Wait for all threads to complete 
for t in threads: 
    t.join() 
print ("Exit Main Thread") 

```