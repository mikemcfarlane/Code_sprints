""" Looking at concurrency. Moving two head motors (pitch and yaw),
    and logging data simultaneously.

"""

# MEMORY_VALUE_NAMES is the list of ALMemory values names you want to save.
ALMEMORY_KEY_NAMES = [
"Device/SubDeviceList/HeadYaw/Position/Sensor/Value",
"Device/SubDeviceList/HeadYaw/Position/Actuator/Value",
"Device/SubDeviceList/HeadYaw/ElectricCurrent/Sensor/Value",
"Device/SubDeviceList/HeadYaw/Temperature/Sensor/Value",
"Device/SubDeviceList/HeadYaw/Hardness/Actuator/Value",
"Device/SubDeviceList/HeadYaw/Temperature/Sensor/Status",
"Device/SubDeviceList/HeadPitch/Position/Actuator/Value",
"Device/SubDeviceList/HeadPitch/Position/Sensor/Value",
"Device/SubDeviceList/HeadPitch/ElectricCurrent/Sensor/Value",
"Device/SubDeviceList/HeadPitch/Temperature/Sensor/Value",
"Device/SubDeviceList/HeadPitch/Hardness/Actuator/Value",
"Device/SubDeviceList/HeadPitch/Temperature/Sensor/Status"
]

# GLOBALS - as easier than passing arguments to timeit
NAO_IP = "mistcalf.local"
STEPS = 5
POSITIVEANGLE = 1.0
NEGATIVEANGLE = -1.0
TESTREPS = 1
TIME = 20.0

POSITIVEANGLESTEP = POSITIVEANGLE / STEPS
NEGATIVEANGLESTEP = NEGATIVEANGLE / STEPS
TIMESTEP = TIME / STEPS
if TIMESTEP <= 0.05:
    # memory.getData() should not be called more than every 50ms as slow.
    print "Warning, TIMESTEP too fast for memory.getData(), set to 50ms."
    TIMESTEP = 0.05

# GLOBALS - proxies and locks
motion = None
posture = None
memory = None
threadLock = None
processLock = None

import time
import threading
import multiprocessing
from timeit import timeit
from naoqi import ALProxy

##########################################################
#                   START test1Procedural CODE
##########################################################

def test1Procedural():
    """ Do some moves and record data in a procedural ie
        linear, method.
        
    """
    global motion, posture, memory
    data = list()    
    
    for i in range(STEPS):
        motion.angleInterpolation(
            ["HeadYaw"],
            [POSITIVEANGLESTEP],
            [TIMESTEP],
            False
        )
        
        motion.angleInterpolation(
            ["HeadPitch"],
            [NEGATIVEANGLESTEP],
            [TIMESTEP],
            False
        )
        
        line = list()
        for key in ALMEMORY_KEY_NAMES:
            value = memory.getData(key)
            line.append(value)
        data.append(line)
        
    #print data
    
##########################################################
#                   END test1Procedural CODE
##########################################################
    
##########################################################
#                   START test2Post CODE
##########################################################
    
def test2Post():
    """ Do some moves and record data using built in post.
        
    """
    global motion, posture, memory  
    
    id1 = motion.post.angleInterpolation(
                                    ["HeadYaw"],
                                    [POSITIVEANGLE],
                                    [TIME],
                                    False
    )
        
    id2 = motion.post.angleInterpolation(
                                    ["HeadPitch"],
                                    [NEGATIVEANGLE],
                                    [TIME],
                                    False
    )
        
    data = recordData()

    while (motion.isRunning(id1) and motion.isRunning(id2)):
        pass
    
    #print data
    
def recordData():
    """ Record the data from ALMemory.
    Returns a matrix of values

    """
    global memory
    
    print "Recording data ..."
    
    data = list()
    for i in range (STEPS):
        line = list()
        for key in ALMEMORY_KEY_NAMES:
            value = memory.getData(key)
            line.append(value)
        data.append(line)
        time.sleep(TIMESTEP)
        
    print "Done recording data"
    
    return data
    
##########################################################
#                   END test2Post CODE
##########################################################

##########################################################
#                   START test3Threading CODE
##########################################################

class myThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID  
        
    def run(self):
        if self.threadID == 1:
            headYawMotion()
        elif self.threadID == 2:
            headPitchMotion()
        elif self.threadID == 3:
            data = recordDataForThread()
            # print data
        else:
            print "oops, no thread"

def headYawMotion():
    global motion, posture, memory, threadLock
    
    for i in range(STEPS):
        threadLock.acquire(True)
        motion.angleInterpolation(
            ["HeadYaw"],
            [POSITIVEANGLESTEP],
            [TIMESTEP],
            False
        )
        threadLock.release()
    
def headPitchMotion():
    global motion, posture, memory, threadLock
    
    for i in range(STEPS):
        threadLock.acquire(True)
        motion.angleInterpolation(
                                ["HeadPitch"],
                                [NEGATIVEANGLESTEP],
                                [TIMESTEP],
                                False
        )
        threadLock.release()
    
def recordDataForThread():
    """ Record the data from ALMemory.
    Returns a matrix of values

    """
    global motion, posture, memory, threadLock
    
    print "Recording data ..."
    
    data = list()
    for i in range (STEPS):
        threadLock.acquire(True)
        line = list()
        for key in ALMEMORY_KEY_NAMES:
            value = memory.getData(key)
            line.append(value)
        data.append(line)
        time.sleep(TIMESTEP)
        threadLock.release()
        
    print "Done recording data"
    
    return data

def test3Threading():
    """ Do some moves and record data using the threading module.
        Runs without Lock(), will use Lock() as best practise,
        and needed in current app.
        Lock.Acquire(False) with Blocking = False arg seems to run smoother, but
        should be set to True to ensure synchronous running. Requires checking.        
        Lock can also be acquired and released using 'with lock:'.
        But without blocking the shared resource does not seem safe.
    
    """
    global motion, posture, memory, threadLock
    
    threads = []
    threadLock = threading.Lock()
    
    # Create new threads.
    thread1 = myThread(1)
    thread2 = myThread(2)
    thread3 = myThread(3)
    
    # Start new threads.
    thread1.start()
    thread2.start()
    thread3.start()
    
    # Wait for threads to end.
    # Essential, or thread calls methods in run, then returns.
    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)
    
    for t in threads:
        t.join()
    
##########################################################
#                   END test3Threading CODE
##########################################################

##########################################################
#                   START test4Multiprocessing CODE
# Doesn't run, issues with proxies causing error:
# 5891 qimessaging.remoteobject: no promise found for req id:39  obj: 21  func: 126 type: 2
##########################################################

def headYawMotionProcess(processLock):
    global motion, posture, memory
    
    for i in range(STEPS):
        processLock.acquire()
        motion.angleInterpolation(
                ["HeadYaw"],
                [POSITIVEANGLESTEP],
                [TIMESTEP],
                False
        )
        processLock.release()
    
def headPitchMotionProcess(processLock):
    global motion, posture, memory
    
    for i in range(STEPS):
        processLock.acquire()
        motion.angleInterpolation(
                            ["HeadPitch"],
                            [NEGATIVEANGLESTEP],
                            [TIMESTEP],
                            False
        )
        processLock.release()
    
def recordDataProcess(processLock):
    """ Record the data from ALMemory.
    Returns a matrix of values

    """
    global motion, posture, memory
    
    print "Recording data ..."
    
    data = list()
    for i in range (STEPS):
        processLock.acquire()
        line = list()
        for key in ALMEMORY_KEY_NAMES:
            value = memory.getData(key)
            line.append(value)
        data.append(line)
        time.sleep(TIMESTEP)
        processLock.release()
        
    print "Done recording data"
    
    print data


def test4Multiprocessing():
    """ Do some moves and record data using the multiprocessing module.
    
    """
    global motion, posture, memory, processLock
    
    processLock = multiprocessing.Lock()
    
    # Spawn process objects.
    p1 = multiprocessing.Process(target = headYawMotionProcess, args = (processLock,))
    p2 = multiprocessing.Process(target = headPitchMotionProcess, args = (processLock,))
    p3 = multiprocessing.Process(target = recordDataProcess, args = (processLock,))
    
    # Start processes.
    p1.start()
    p2.start()
    p3.start()
    
    # Wait for processes to finish.
    p1.join()
    p2.join()
    p3.join()


##########################################################
#                   END test4Multiprocessing CODE
##########################################################

##########################################################
#                   START test5Coroutine CODE
##########################################################

def headYawMotionCoroutine(yawMotionList):
    global motion, posture, memory
    
    _yawMotionList = list(yawMotionList)
    current = 0
    
    while len(_yawMotionList):
        angle = _yawMotionList[current][0]
        time = _yawMotionList[current][1]
        motion.angleInterpolation(
                    ["HeadYaw"],
                    [angle],
                    [time],
                    False
        )
        yield
        current += 1

    
def headPitchMotionCoroutine(pitchMotionList):
    global motion, posture, memory
    
    _pitchMotionList = list(pitchMotionList)
    current = 0
    
    while len(_pitchMotionList):
        angle = _pitchMotionList[current][0]
        time = _pitchMotionList[current][1]
        motion.angleInterpolation(
                                ["HeadPitch"],
                                [angle],
                                [time],
                                False
        )
        yield
        current += 1
    
def recordDataCoroutine():
    """ Record the data from ALMemory.
    Returns a matrix of values

    """
    global motion, posture, memory
    
    print "Recording data ..."
    
    data = list()
    # Infinite list as is run every time there is a motion move.
    while 1:        
        line = list()
        for key in ALMEMORY_KEY_NAMES:
            value = memory.getData(key)
            line.append(value)
        data.append(line)
        yield data
        
def test5Coroutine():
    """ Do some moves and record data using coroutines.
    
    """
    global motion, posture, memory
    
    # Generate motion lists
    yawMotionList = []
    pitchMotionList = []            
    yawMotionList = [(POSITIVEANGLESTEP, TIMESTEP) for i in range(STEPS)]
    pitchMotionList = [(NEGATIVEANGLESTEP, TIMESTEP) for i in range(STEPS)]
    
    # Ininitiate coroutine.
    p1 = headYawMotionCoroutine(yawMotionList)
    p2 = headPitchMotionCoroutine(pitchMotionList)
    p3 = recordDataCoroutine()

    # Loop through all steps. Could also be infinite loop if this was,
    # a full coroutine where data was being sent to the lists.
    for i in range(STEPS):
        p1.next()
        p2.next()
        data = p3.next()
        
    #print data
    

##########################################################
#                   END test5Coroutine CODE
##########################################################

def main():
    """ Some simple robot processes.

    """
    global motion, posture, memory

    motion = ALProxy("ALMotion", NAO_IP, 9559)
    posture = ALProxy("ALRobotPosture", NAO_IP, 9559)
    memory = ALProxy("ALMemory", NAO_IP, 9559)    

    # Set stiffness on for Head motors and go to start pose.
    print "Starting tests...."
    motion.setStiffnesses("Head", 1.0)
    print "\n---------------------------------------\n"
    # Goto start position, and run test1Procedural
    print "test1Procedural starting ..."
    posture.goToPosture("Crouch", 2.0)
    t1 = (timeit("test1Procedural()", setup = "from __main__ import test1Procedural", number = TESTREPS))
    print "...end test1Procedural, time: ", t1
    print "\n---------------------------------------\n"
    # Goto start position, and run test2Post
    print "test2Post starting ..."
    posture.goToPosture("Crouch", 2.0)
    t2 = (timeit("test2Post()", setup = "from __main__ import test2Post", number = TESTREPS))
    print "...end test2Post, time: ", t2
    print "\n---------------------------------------\n"
    # Goto start position, and run test3Threading
    print "test3Threading starting ..."
    posture.goToPosture("Crouch", 2.0)
    t3 = (timeit("test3Threading()", setup = "from __main__ import test3Threading", number = TESTREPS))
    print "...end test3Threading, time: ", t3
    print "\n---------------------------------------\n"
    # Goto start position, and run test4Multiprocessing - NOT WORKING
    print "test4Multiprocessing - not working"
    #print "test4Multiprocessing starting ..."
    #posture.goToPosture("Crouch", 2.0)
    #test4Multiprocessing()
    #t4 = (timeit("test4Multiprocessing()", setup = "from __main__ import test3Threading", number = TESTREPS))
    #print "...end test4Multiprocessing, time: ", t4
    print "\n---------------------------------------\n"
    # Goto start position, and run test5Coroutine
    print "test5Coroutine starting ..."
    posture.goToPosture("Crouch", 2.0)
    t5 = (timeit("test5Coroutine()", setup = "from __main__ import test5Coroutine", number = TESTREPS))
    print "...end test5Coroutine, time: ", t5
    print "\n---------------------------------------\n"
    # Gently set stiff off for Head motors and relax.
    print "...ending tests!"
    motion.setStiffnesses("Head", 0.0)
    motion.rest()
    
if __name__ == "__main__":
    main()