"""emitter controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

import struct
from controller import DistanceSensor
from controller import Emitter
from controller import Motor
from controller import Receiver

SPEED = 6
TIME_STEP = 64
COMMUNICATION_CHANNEL = 1

robot = Robot()

receiver = Receiver("Receiver")

message_printed = 0

wheels = []
wheelsNames = ['wheel1', 'wheel2']
for i in range(2):
    wheels.append(robot.getMotor(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)


robot_type = 1
communication = robot.getReceiver("Receiver")
Receiver.enable(communication, TIME_STEP)

  
  
ds0 = robot.getDistanceSensor("ds0")
ds1 = robot.getDistanceSensor("ds1")
ds0.enable(TIME_STEP)
ds1.enable(TIME_STEP)
# Main loop:

while robot.step(TIME_STEP) != -1:

    # Just receiver stuff...
    if (Receiver.getQueueLength(communication) > 0) :
        # /* read current packet's data */

        new_message= receiver.getData()
        message = struct.unpack("ddd", new_mssage)

        if (message_printed != 1) :
          # /* print null-terminated message */
          print(f"{message[0]} {message[1]} {message[2]}")
          message_printed = 1
            
        # /* fetch next packet */
        Receiver.nextPacket(communication)
    else :
        if (message_printed != 2) :
          print("Communication broken!\n")
          message_printed = 2
    
    ds0_value = DistanceSensor.getValue(ds0)
    ds1_value = DistanceSensor.getValue(ds1)
    
    if (ds1_value > 500) :
        # /*
         # * If both distance sensors are detecting something, this means that
         # * we are facing a wall. In this case we need to move backwards.
         # */
        if (ds0_value > 200) :
            left_speed = -SPEED / 2
            right_speed = -SPEED
      
        else :
          # /*
           # * we turn proportionnaly to the sensors value because the
           # * closer we are from the wall, the more we need to turn.
           # */
          left_speed = -ds1_value / 100
          right_speed = (ds0_value / 100) + 0.5
          
    elif (ds0_value > 500) :
        left_speed = (ds1_value / 100) + 0.5
        right_speed = -ds0_value / 100
    else :
        # /*
         # * if nothing was detected we can move forward at maximal speed.
         # */
        left_speed = SPEED
        right_speed = SPEED
    
    
        # /* set the motor speeds. */
    wheels[0].setVelocity(left_speed)
    wheels[1].setVelocity(right_speed)
    