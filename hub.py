import socket
import time
import _thread
import datetime
import Adafruit_DHT
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
from rpi_rf import RFDevice

MQTT_SERVER = "18.203.92.71"
DEVICE_PATH = "DEVICES"
TOGGLE_PATH = "Toggle"

Heat = 0
Light = 0
Blanket = 0
Temp = 00
MinTemp = 20
MaxTemp = 22

def ControlSockets():
    
    global Heat
    global Light
    global Blanket
    global Temp
    global MinTemp
    global MaxTemp
    
    Radio = RFDevice(17)
    Radio.enable_tx()

    MainHeatOn = 5330227
    MainHeatOff = 5330236
    BoostHeatOn = 5332227
    BoostHeatOff = 5332236
    LightOn = 5330691
    LightOff = 5330700
    BlanketOn = 5330371
    BlanketOff = 5330380
      
    PIN = 189
        
    while True:
        
        if  Heat == 0 or int(Temp) > MaxTemp:            
            Radio.tx_code(MainHeatOff, 1, PIN)
        
        elif Heat == 1 and int(Temp) < MaxTemp:           
            Radio.tx_code(MainHeatOn, 1, PIN)
        
        time.sleep(0.1)
        
        if  Heat == 0 or int(Temp) > MinTemp:            
            Radio.tx_code(BoostHeatOff, 1, PIN)
        
        elif Heat == 1 and int(Temp) < MinTemp:           
            Radio.tx_code(BoostHeatOn, 1, PIN)
        
        time.sleep(0.1)
        
        if  Light == 0:            
            Radio.tx_code(LightOff, 1, PIN)
        
        elif Light == 1:            
            Radio.tx_code(LightOn, 1, PIN)
            
        time.sleep(0.1)
            
        if  Blanket == 0:           
            Radio.tx_code(BlanketOff, 1, PIN)
        
        elif Blanket == 1:            
            Radio.tx_code(BlanketOn, 1, PIN)
        
        time.sleep(0.1)

def SensorReadings():
    
    global Temp
    
    #temp values for tracking updates
    CTemp = Temp
    
    while True:
        
        #attempt to get data from the sensor module
        X, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22,27)
        
        #convert to integers
        if T is not None:       
            T = round(T,1)
            print(T)
            #If between 0 and 99 and the first reading, or between 0 and 99 and the reading has changed but not more than 25%
            if T >= 0 and T < 100 and CTemp == 0 or T >= 0 and T < 100 and T < CTemp*1.25 and T > CTemp*0.75:

                #update relevent values 
                Temp = T
                CTemp = T
                
            PublishtoDevices()
            time.sleep(10)
            
def PublishtoDevices():
    
    global Heat
    global Light
    global Blanket
    global Temp
    global MinTemp
    global MaxTemp
    
    Data = str(Heat)+","+str(Light)+","+str(Blanket)+","+str(Temp)+","+str(MinTemp)+","+str(MaxTemp)
    publish.single(DEVICE_PATH, Data, hostname=MQTT_SERVER)
           
#start listening and sensor threads
_thread.start_new_thread(ControlSockets, ())
_thread.start_new_thread(PublishtoDevices, ())
_thread.start_new_thread(SensorReadings, ())

#startup complete status message
print ("Online at",datetime.datetime.now().strftime("%I:%M:%S %p"))

def ToggleHeat():
    
    global Heat
    
    if Heat == 1:
        Heat = 0
        print('Heat Off')
    
    else:
        Heat = 1
        print('Heat On')
         
    PublishtoDevices()
        
def ToggleBoostHeat():
    
    global BoostHeat
    
    if BoostHeat == 1:
        BoostHeat = 0
        print('BoostHeat Off')
    
    else:
        BoostHeat = 1
        print('BoostHeat On')
        
    PublishtoDevices()
        
def ToggleLight():
    
    global Light
    
    if Light == 1:
        Light = 0
        print('Light Off')
    
    else:
        Light = 1
        print('Light On')
        
    PublishtoDevices()
        
def ToggleBlanket():
    
    global Blanket
       
    if Blanket == 1:
        Blanket = 0
        print('Blanket Off')
    
    else:
        Blanket = 1
        print('Blanket On')
        
    PublishtoDevices()
    
def ToggleThermostat():

    global MinTemp
    global MaxTemp
    
    if MinTemp is 19:
        MinTemp = 20
        MaxTemp = 22
        print('Thermometer Medium')
        
    elif MinTemp is 20:
        MinTemp = 21
        MaxTemp = 23
        print('Thermometer High')
        
    elif MinTemp is 21:
        MinTemp = 22
        MaxTemp = 24
        print('Thermometer Full')
        
    elif MinTemp is 22:
        MinTemp = 19
        MaxTemp = 21
        print('Thermometer Low')
    
    PublishtoDevices()
    
def on_connect(client, userdata, flags, rc):
     
    client.subscribe(TOGGLE_PATH)
    
def on_message(client, userdata, msg):
       
    Request = str(msg.payload)
  
    if Request[2] == '1':   
        ToggleHeat()
        
    elif Request[2] == '2':
        ToggleLight()
        
    elif Request[2] == '3':      
        ToggleBlanket()
        
    elif Request[2] == '4':       
        ToggleThermostat()
        
    else:
        PublishtoDevices()
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 15)
client.loop_forever()
