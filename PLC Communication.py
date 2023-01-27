import snap7
from snap7.util import *
import modbus
import time

'''
DB 500
int alarm= 2.0
int status=4.0
bool fault reset=6.0
bool run_trigger=6.1
bool home=6.2
bool fwd= 6.3
bool rev= 6.4
bool hearbeat= 10.0
'''
plc = snap7.client.Client()
db= 500

try:
    plc.connect('192.168.0.10',0,1)
    init = True
    print('plc connected')
    plc.db_write(db, 6, b'\0')
except:
    print('Plc disconnected')
    init= False
modbus.stopJog()
modbus.resetAlarm()
a=0

while init:
    write_trigger=b'\0'
    
    try:
        
        trigger = plc.db_read(db, 6, 1)
        old_trigger=bytearray(trigger)
        fr= get_bool(trigger,0,0)
        run= get_bool(trigger, 0, 1)
        home= get_bool(trigger, 0, 2)
        fwd= get_bool(trigger, 0, 3)
        rev= get_bool(trigger, 0, 4)
        hb = plc.db_read(db, 10, 1)
        heartbeat= get_bool(hb, 0, 0)
        test= get_bool(hb, 0, 1)
        speed= 240 


        if fr: 
            print("[", time.time(), "]\tFault Reset")
            # print(trigger)
            modbus.resetAlarm()
            set_bool(trigger,0,0,0)
            fr=0

        if run: 
            print("[", time.time(), "]\tRun")
            print(trigger)
            modbus.setPosition(-10000,speed,1)
            set_bool(trigger,0,1,0)
            # plc.db_write(db,6,b'0')
            run=0

        if home: 
            print("[", time.time(), "]\thome")
            # print(trigger)
            modbus.seekHome()
            modbus.stopJog()
            set_bool(trigger,0,2,0)
            # plc.db_write(db,6,b'0')
            home=0

        if fwd and a!=3:
            print("[", time.time(), "]\tforward jog")
            modbus.setSpeed(100,1)
            modbus.startJog()
            a=3
        elif rev and a!=4:
            print("[", time.time(), "]\tReverse Jog")
            print(trigger, rev)
            modbus.setSpeed(-100,1)
            modbus.startJog()
            a=4
        elif not fwd and not rev and a!=0:
            print("[", time.time(), "]\tno jog")
            modbus.stopJog()
            a=0
        if heartbeat:
            # print("heartbeat")
            heartbeat=0
            plc.db_write(db,10,b'0')

        alarm,alarm_list= modbus.readAlarm(1)
        status, status_list= modbus.getStatus(1)


        alarm_array=alarm.to_bytes(2,'big')
        # print("Alarm= ", alarm, "Alarm_array", alarm_array)
        plc.db_write(db,2,alarm_array)

        status_array=status.to_bytes(2,'big')
        # print("Status= ", status, "Status array= ", status_array)
        plc.db_write(db,4,status_array)
        if trigger!= old_trigger:
            # print("old is not new")
            plc.db_write(db, 6, trigger)
            old_trigger=trigger
    except:
        print("[", time.time(), "]\tPLC communication error")
        continue

