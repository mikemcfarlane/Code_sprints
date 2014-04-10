
""" Record some sensors values and write them into a file.

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

nao_ip = "mistcalf.local"

import os
import sys
import time

from naoqi import ALProxy

memory = None
motion = None
posture = None

def recordData(nao_ip):
    """ Record the data from ALMemory.
    Returns a matrix of values

    """
    global memory
    global motion
    
    print "Recording data ..."
    
    data = list()
    for i in range (1, 100):
        line = list()
        for key in ALMEMORY_KEY_NAMES:
            value = memory.getData(key)
            line.append(value)
        data.append(line)
        time.sleep(0.01)
        
    print "Done recording data"
    
    return data

def postTest(headYawList, headPitchList):
    """ Test concurrency using built in post object to start another thread.
    
    """
    global memory
    global motion
    
    nameYaw = headYawList[0]
    angleListYaw = headYawList[1]
    timeListYaw = headYawList[2]
    isAbsoluteYaw = headYawList[3]
    
    namePitch = headPitchList[0]
    angleListPitch = headPitchList[1]
    timeListPitch = headPitchList[2]
    isAbsolutePitch = headPitchList[3]
    
    # Set stiffness on for Head motors
    motion.setStiffnesses("Head", 1.0)
    
    id1 = motion.post.angleInterpolation(nameYaw, angleListYaw, timeListYaw, isAbsoluteYaw)
    id2 = motion.post.angleInterpolation(namePitch, angleListPitch, timeListPitch, isAbsolutePitch)
    data = recordData(nao_ip)
    while (motion.isRunning(id1) and motion.isRunning(id2)):
        pass
    
    print "Finished move."
    
    # Gently set stiff off for Head motors
    motion.setStiffnesses("Head", 0.0)

    output = os.path.abspath("record.csv")

    with open(output, "w") as fp:
        for line in data:
            fp.write("; ".join(str(x) for x in line))
            fp.write("\n")

    print "Results written to", output
    
def generateLists():
    timeList = []
    moveList = []
    reverseMoveList = []
    totalMoveList = []
    steps = 100.0
    totalTime = 20.0
    totalMove = 1.0
    for i in range(int(steps)):
        timeList.append(totalTime / steps * i + totalTime / steps)
    for i in range(int(steps/2)):
        moveList.append(totalMove / (steps/2) * i + totalMove / (steps/2))
    reverseMoveList = list(moveList)
    reverseMoveList.reverse()
    reverseMoveList[:] = [i - totalMove / (steps/2) for i in reverseMoveList]
    totalMoveList = moveList + reverseMoveList
    return timeList, totalMoveList

def main():
    """ Run some timing tests on concurrent methods.

    """
    from timeit import timeit
    
    global memory
    global motion
    global posture

    motion = ALProxy("ALMotion", nao_ip, 9559)
    memory = ALProxy("ALMemory", nao_ip, 9559)
    posture = ALProxy("ALRobotPosture", nao_ip, 9559)
    
    # Test 1 with post for two threaded motion calls.
    posture.goToPosture("Crouch", 2.0)
    timeList, moveList = generateLists()
    headYawList = ["HeadYaw", moveList, timeList, False]
    headPitchList = ["HeadPitch", moveList, timeList, False]
    t = (timeit("postTest(%s, %s)" % (headYawList, headPitchList), setup="from __main__ import postTest", number = 1))
    print "Test 1 with post took (s): ", t
    posture.goToPosture("Crouch", 2.0)
    motion.rest()
    
if __name__ == "__main__":
    main()