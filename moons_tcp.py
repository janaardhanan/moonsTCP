#! /usr/bin/env python3

import modbus
import time

print("modbus_tcp.py")

print("STEPS PER REVOLUTION: ", modbus.readRegister(52, 1, 0))
print("VELOCITY: ", modbus.readRegister(48, 1, 0))
# modbus.writeRegister(29, 480, 1)
# modbus.setPosition(200000,1)
# print(modbus.getEncoder(1,-2000))
# for i in range(0,6):
    
#     time.sleep(1)
#     print(i+1, end=" ")
#     print(modbus.getEncoder(1,-2000))0
# print()
# print(modbus.getEncoder(1,-2000))
# print(modbus.getEncoder(1,-2000))

# modbus.setPosition(0,1)
# time.sleep(6)
# print(modbus.getEncoder(1,-2000))

modbus.writeRegister(48, 0xf0,1)
modbus.writeRegister(124, 0xe2,1)
a=[]

while(False):
    a= int(input("enter position: "))
    print(modbus.getEncoder(1,-2000))

    modbus.setPosition(a,1)
# modbus.setPosition(5000,1)
# time.sleep(3)
# modbus.setPosition(1000,1)
# time.sleep(3)
# modbus.setPosition(0,1)