import snap7
from snap7.util import *
import modbus

'''
DB 500
int alarm= 2.0
int status=4.0
bool fault reset=6.0
bool run_trigger=6.1
bool home=6.2
'''

plc = snap7.client.Client()
db= 500

try:
	plc.connect('192.168.0.10',0,1)
	print('plc connected')
except:
	print('Plc disconnected')
modbus.stopJog()

while True:
    write_trigger=b'0'
    
    try:
        
        trigger = plc.db_read(db, 6, 1)
        fr= get_bool(trigger,0,0)
        run= get_bool(trigger, 0, 1)
        home= get_bool(trigger, 0, 2)
        trigger = plc.db_read(db, 10, 1)
        heartbeat= get_bool(trigger, 0, 0)
        speed= 240 


        if fr: 
            print("Fault Reset")
            print(trigger)
            modbus.resetAlarm()
            fr=0
        if run: 
            print("Run")
            print(trigger)
            modbus.setPosition(-10000,speed,1)
            plc.db_write(db,6,b'0')
            run=0
        if home: 
            print("home")
            print(trigger)
            modbus.seekHome()
            modbus.stopJog()
            plc.db_write(db,6,b'0')
            home=0
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
    except:
        print("PLC communication error")
        continue
    
