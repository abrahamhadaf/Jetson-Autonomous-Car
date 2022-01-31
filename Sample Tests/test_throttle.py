from adafruit_servokit import ServoKit
import board
import busio
import time
from approxeng.input.selectbinder import ControllerResource
    
print("Initializing Servos")
i2c_bus1=(busio.I2C(board.SCL, board.SDA))
print("Initializing ServoKit")
kit = ServoKit(channels=16, i2c=i2c_bus1)
# kit[0] is the bottom servo
# kit[1] is the top servo
print("Done initializing")

## Minimum speed for Throttle use channel 1 for Servo angles and channel 0 for throttle
#kit.servo[0].angle = 100
time.sleep(1)
kit.servo[0].angle = 0
time.sleep(1)
