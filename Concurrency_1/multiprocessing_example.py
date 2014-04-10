from multiprocessing import Process, Lock
import time
    
def print_time(processName, counter, delay, lock, increment):
    global TESTNUM
    
    while counter:
        lock.acquire()
        TESTNUM += increment
        time.sleep(delay)
        print "%s: %s with TESTNUM: %s" % (processName, time.ctime(time.time()), TESTNUM)
        counter -= 1
        TESTNUM -= increment
        if TESTNUM != 0:
            print "Shared resource was accessed by both processes!"
        lock.release()
    
if __name__ == '__main__':
    counter = 10
    delay = 0.5
    TESTNUM = 0
    
    lock = Lock()
    
    # Spawn process objects.
    p1 = Process(target = print_time, args = ('process1', counter, delay, lock, 1))
    p2 = Process(target = print_time, args = ('process2', counter, delay, lock, 2))
    
    # Start processes.
    p1.start()
    p2.start()
    
    # Wait for processes to finish.
    p1.join()
    p2.join()