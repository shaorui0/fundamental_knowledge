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