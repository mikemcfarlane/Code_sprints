import threading
import time

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter, delay, threadLock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.delay = delay
        self.threadLock = threadLock
        
    def run(self):
        global TESTNUM, THREADERROR
        print "Starting " + self.name
        # Get lock to synchronize threads
        # nb use of blocking = False arg to allow threads to run in parallel.
        self.threadLock.acquire(BLOCKING)
        
        while self.counter:
            time.sleep(self.delay)
            TESTNUM += self.threadID
            #print "TESTNUM BEFORE: ", TESTNUM
            print "%s: %s" % (self.name, time.ctime(time.time()))
            self.counter -= 1
            TESTNUM -= self.threadID
            if TESTNUM != 0:
                print "Shared resource was accessed by both threads!"
                THREADERROR = 1
                
        # Free lock to release next thread
        try:
            self.threadLock.release()
        except Exception, e:
            print "Error releasing threadlock: ", e

            
def runLockTest(counter, delay, threadLock):
    # Create new threads
    thread1 = myThread(1, "Thread-1", counter, delay, threadLock)
    thread2 = myThread(2, "Thread-2", counter, delay, threadLock)

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
delay = 1
runLockTest(counter, delay, threadLock)

# Test with Lock() blocking disabled.
print "Running with Lock() blocking = False"
threadLock = threading.Lock()
threads = []
BLOCKING = False
TESTNUM = 0
THREADERROR = 0
counter = 10
delay = 1
runLockTest(counter, delay, threadLock)     