import threading
import queue
import time

class BoundedBlockQueue(object):
    def __init__(self, max_size):
        self.max_size = max_size
        self.lock = threading.Lock()

        self.not_empty = threading.Condition(self.lock)
        self.not_full = threading.Condition(self.lock)
        self.queue = []

    def qsize(self):
        return len(self.queue)

    def full(self):
        return len(self.queue) == self.max_size

    def empty(self):
        return len(self.queue) == 0

    def take(self):
        self.not_empty.acquire()

        while self.empty(): # always use a while-loop, due to spurious wakeup
            self.not_empty.wait()

        assert not self.empty()
        item = self.queue[0]
        self.queue.remove(item)

        self.not_full.notify()

        self.not_empty.release()

        return item

    def put(self, item):
        self.not_full.acquire()

        while self.full(): # always use a while-loop, due to spurious wakeup
            self.not_full.wait()

        assert not self.full()
        self.queue.append(item)
        print(self.queue)

        self.not_empty.notify()

        self.not_full.release()
    
    def join(self):
        # TODO too simple to implement
        while not self.empty():
            pass


q = BoundedBlockQueue(10)

def worker():
    while True:
        item = q.take()
        print(f'Working on {item}')
        print(f'Finished {item}')
        time.sleep(0.1)


# turn-on the worker thread
threading.Thread(target=worker, daemon=False).start()

# send thirty task requests to the worker
for item in range(30):
    print(item)
    q.put(item)

print('All task requests sent\n', end='')

# block until all tasks are done
q.join()
print('All work completed')
import os 
os._exit(0)
