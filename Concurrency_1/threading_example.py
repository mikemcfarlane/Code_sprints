import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.delay = delay
    def run(self):
        print "Starting " + self.name
        print_time(self.name, self.counter, self.delay)
        print "Exiting " + self.name

def print_time(threadName, counter, delay):
    while counter:
        if exitFlag:
            print "%s exited." % threadName
            thread.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1

# Create new threads
counter = 10
delay = 0.5
thread1 = myThread(1, "Thread-1", counter, delay)
thread2 = myThread(2, "Thread-2", counter, delay)

# Start new Threads
thread1.start()
thread2.start()

print "Exiting Main Thread"