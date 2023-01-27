#! /usr/bin/env python3

import modbus
import time

print("modbus_tcp.py")

print("STEPS PER REVOLUTION: ", modbus.readRegister(52, 1, 0))
print("VELOCITY: ", modbus.readRegister(48, 1, 0))

print("forward jog")
modbus.setSpeed(100,1)
modbus.startJog()


# try:
#     time.sleep(2)
#     print(modbus.getSpeed(1,-2000))
#     print("reverse jog")
#     modbus.setSpeed(-240,1)
     
# except:
#     pass
# time.sleep(2)
# print(modbus.getSpeed(1,-2000))
input("enter something to stop")
modbus.stopJog()
print("Stopped jog")


# print(modbus.readAlarm(1))
# print(modbus.getStatus(1))

# modbus.resetAlarm()
# print(modbus.readAlarm(1))


# modbus.seekHome()

# print("homing done")
# print("Encoder value: ", modbus.getEncoder(1,-2000))
# modbus.setEncoder(1,0)
# print("Encoder value: ", modbus.getEncoder(1,-2000))

# time.sleep(1)

# while True:
#     input("enter something ")
#     modbus.setPosition(-10000,1)
#     time.sleep(1)
