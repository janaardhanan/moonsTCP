#!/usr/bin/python3
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder as dec
from pymodbus.constants import Endian
import time

def two_cmp(val, bits):
    if val > 2**(bits-1):
            #val = val - 4294967296
            val= val-2**bits
    return val

def getBits(val, bits):
    bit_list=[]
    if val>0:
        for i in range(0, bits):
            if val & 2**i == 2**i:
                bit_list.append(i)
    return bit_list

def end():
    stopJog()
    print("close connection")
    mod.close()


#--------------------------------------


def readRegister(add, ids, mode):
    global motor_status
    try:
        read= mod.read_holding_registers(address= add, count= 1, unit= ids)
        read0= read.getRegister(0)
        if mode==1:
            return(two_cmp(read0, 16))
        motor_status=1
        return(read0)
    except:
        motor_status=0
        return 0
        

def longRead(add, ids, mode, prev):
    global motor_status
    try:
        result= mod.read_holding_registers(address= add, count=2, unit= ids)
        decoder= dec.fromRegisters(result.registers, Endian.Big)
        motor_status=1
        return(decoder.decode_32bit_int())

    except AttributeError as e:
        print("error1: ", e, end= " \t")
        print("prev= ", prev)
        motor_status=0
        return prev

    '''
    value= mod.read_holding_registers(address= add, count=2, unit= ids)
    en0 = abs(value.getRegister(1))
    en1= abs(value.getRegister(0)*(2**16))
    en_value= (en0+ en1)
    if mode==1:
        return(two_cmp(en_value, 32))
    '''
    
    

def writeRegister(add, val, ids):
    global motor_status
    val= (val+ (1<<16))%(1<<16)
    print("write register: ", val)
    rd= mod.write_register(address= add, value= val, unit=ids)
    motor_status=1

def longWrite(add, value, ids):
    global motor_status
    val= (value+ (1<<32))%(1<<32)
    msb= (val>>16)
    lsb= (val& 65535)
    r1= mod.write_registers(address= add, values= [msb, lsb], unit= ids)
    motor_status=1
#--------------------------------------------------------------------

def startJog():
    global motor_status
    writeRegister(124, 159, 1)

    writeRegister(124, 150, 1)
    print("Jog started")

def stopJog():
    writeRegister(124, 226, 1)
    print("Jog Stopped")    

def readAlarm(ids):
    #val1= readRegister(0, ids,0)
    #val2= readRegister(1, ids,0)
    val= readRegister(0, ids,0)
    # print("Alarm Value: ",val)
    alarms= {0:"position error overrun", 1:"reverse prohibition limit", 2:"positive prohibition limit", 3:"over temperature", 4:"internal error", 5:"supply voltage out of range", 6:"reserved", 7:"drive overcurrent", 8:"reserved", 9:"motor encodeer not connected",
             10:"communication exception", 11:"reserved", 12:"vent failure", 13:"motor overload protection", 14:"reserved", 15:"unsuaal start alarm"}
   
    error= getBits(val,16)

    for i in error:
        print(alarms[i], end= ", ")
        
    return val, error

def seekHome():
    writeRegister(125, 0x34, 1)
    writeRegister(126, 0x46, 1)
    writeRegister(124, 0x6e, 1)
    while True:
        x,y=getStatus(1)
        if 10 not in y:
            break

def resetAlarm():
    writeRegister(124, 186, 1)

def brakeStatus(ids):

    val= readRegister(4, ids,0)
    #print(ids, val)
    if val & 4 == 4:
        return True
    return False

    

def setSpeed(speed, ids):
    # print(hex(two_cmp(speed,16)))
    writeRegister(48, speed, ids)

def getSpeed(ids,prev):
    return readRegister(48, ids, 0)

def getEncoder(ids,prev):
    return longRead(4, ids, 0,prev)

def setEncoder(ids, prev):
    # print(getEncoder(ids,prev))
    longWrite(125, prev, ids)
    longRead(125,1,0,-2000)
    writeRegister(124, 0x98, ids)
    # print(getEncoder(ids, prev))

def setPosition(pos,speed, ids):
    longWrite(30,pos, ids)
    writeRegister(29,speed,ids)
    writeRegister(124, 0x66, 1)
    # print(longRead(30,1,0,-2000))

def getCurrent(ids):
    return longRead(30, ids, 0,0)

def getStatus(ids):
    val= readRegister(1, ids,0)
    # print("Status Code: ", val)
    lst= getBits(val,16)
    return val, lst



mod = ModbusTcpClient('192.168.0.140')
print("Connection status: ",mod.connect())
time.sleep(0.2)
