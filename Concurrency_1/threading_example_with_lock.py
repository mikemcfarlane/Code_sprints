import threading
import time

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.delay = delay
        
    def run(self):
        print "Starting " + self.name
        # Get lock to synchronize threads
        # nb use of blocking = False arg to allow threads to run in parallel.
        threadLock.acquire(BLOCKING)
        print_time(self.name, self.counter, self.delay, self.threadID)
        # Free lock to release next thread
        try:
            threadLock.release()
        except Exception, e:
            print "Error releasing threadlock: ", e
        
def print_time(threadName, counter, delay, increment):
    global TESTNUM, THREADERROR
    
    while counter:
        time.sleep(delay)
        TESTNUM += increment
        #print "TESTNUM BEFORE: ", TESTNUM
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1
        TESTNUM -= increment
        if TESTNUM != 0:
            print "Shared resource was accessed by both threads!"
            THREADERROR = 1
            
def runLockTest(counter, delay):   

    # Create new threads
    thread1 = myThread(1, "Thread-1", counter, delay)
    thread2 = myThread(2, "Thread-2", counter, delay)

    # Start new Threads
    thread1.start()
    thread2.start()

    # Add threads to thread list
    threads.append(thread1)
    threads.append(thread2)

    # Wait for all threads to complete
    for t in threads:
        t.join()
    print "Exiting Main Thread"
    if THREADERROR == 0:
        print "Shared resource properly accessed!"
        
# Test with Lock() blocking enabled.
print "Running with Lock() blocking = True"
threadLock = threading.Lock()
threads = []
BLOCKING = True
TESTNUM = 0
THREADERROR = 0
counter = 10
delay = 0.5
runLockTest(counter, delay)

# Test with Lock() blocking disabled.
print "Running with Lock() blocking = False"
threadLock = threading.Lock()
threads = []
BLOCKING = False
TESTNUM = 0
THREADERROR = 0
counter = 10
delay = 0.5
runLockTest(counter, delay)       