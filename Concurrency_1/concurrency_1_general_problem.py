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

NAO_IP = "mistcalf.local"
STEPS = 5

from naoqi import ALProxy

def main():
    """ Some simple robot processes.

    """
    
    motion = ALProxy("ALMotion", NAO_IP, 9559)
    posture = ALProxy("ALRobotPosture", NAO_IP, 9559)
    memory = ALProxy("ALMemory", NAO_IP, 9559)
    
    data = list()
    
    # Set stiffness on for Head motors and go to start pose.
    print "Starting move...."
    motion.setStiffnesses("Head", 1.0)
    posture.goToPosture("Crouch", 2.0)
        
    # Core processes. Do some moves and record data.
    for i in range(STEPS):
        positiveAngleStep = 1.0 / STEPS
        negativeAngleStep = -1 * positiveAngleStep
        timeStep = 20 / STEPS
        motion.angleInterpolation(
            ["HeadYaw"],
            [positiveAngleStep],
            [timeStep],
            False
        )
        
        motion.angleInterpolation(
            ["HeadPitch"],
            [negativeAngleStep],
            [timeStep],
            False
        )
        
        line = list()
        for key in ALMEMORY_KEY_NAMES:
            value = memory.getData(key)
            line.append(value)
        data.append(line)
            
    # Gently set stiff off for Head motors and relax.
    print "...Going to stop now!"
    motion.setStiffnesses("Head", 0.0)
    motion.rest()
    print data
    
if __name__ == "__main__":
    main()