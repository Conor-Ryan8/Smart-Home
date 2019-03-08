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

MainHeat = 0
BoostHeat = 0
Light = 0
Blanket = 0
Temp = 00
Humid = 00


def ControlSockets():   
    
    global MainHeat
    global BoostHeat
    global Light
    global Blanket
    global Temp
    
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
        
        if  MainHeat == 0:            
            Radio.tx_code(MainHeatOff, 1, PIN)
        
        elif MainHeat == 1:           
            Radio.tx_code(MainHeatOn, 1, PIN)
        
        time.sleep(0.1)
        
        if  BoostHeat == 0:            
            Radio.tx_code(BoostHeatOff, 1, PIN)
        
        elif BoostHeat == 1:           
            Radio.tx_code(BoostHeatOn, 1, PIN)
        
        time.sleep(0.1)
        
        if  Light == 0 or Temp > 25:            
            Radio.tx_code(LightOff, 1, PIN)
        
        elif Light == 1 and Temp < 25:            
            Radio.tx_code(LightOn, 1, PIN)
            
        time.sleep(0.1)
            
        if  Blanket == 0:           
            Radio.tx_code(BlanketOff, 1, PIN)
        
        elif Blanket == 1:            
            Radio.tx_code(BlanketOn, 1, PIN)
        
        time.sleep(0.1)

def SensorReadings():
    
    global Temp
    global Humid
    
    #temp values for tracking updates
    CTemp = Temp
    CHumid = Humid
    
    while True:
        
        #attempt to get data from the sensor module
        X, Y = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22,27)
        #convert to integers
        
        if X is not None and Y is not None:       
            T = int(Y)
            H = int(X)
        
            #If between 0 and 99 and the first reading, or between 0 and 99 and the reading has changed but not more than 25%
            if H >= 0 and H < 100 and CHumid == 0 or H >= 0 and H < 100 and H < CHumid*1.25 and H > CHumid*0.75:
             
                #update relevent values 
                Humid = H
                CHumid = H
                print('Humidity: '+str(Humid)+'%')              
         
            #If between 0 and 99 and the first reading, or between 0 and 99 and the reading has changed but not more than 25%
            if T >= 0 and T < 100 and CTemp == 0 or T >= 0 and T < 100 and T < CTemp*1.25 and T > CTemp*0.75:

                #update relevent values 
                Temp = T
                CTemp = T
                print('Temperature: '+str(Temp)+' Degrees')
                
            PublishtoDevices()
            time.sleep(10)
            
def PublishtoDevices():
    
    global MainHeat
    global BoostHeat
    global Light
    global Blanket
    global Temp
    global Humid
    
    Data = str(MainHeat)+","+str(BoostHeat)+","+str(Light)+","+str(Blanket)+","+str(Temp)+","+str(Humid)
    publish.single(DEVICE_PATH, Data, hostname=MQTT_SERVER)
           
#start listening and sensor threads
_thread.start_new_thread(ControlSockets, ())
_thread.start_new_thread(PublishtoDevices, ())
_thread.start_new_thread(SensorReadings, ())

#startup complete status message
print ("Online at",datetime.datetime.now().strftime("%I:%M:%S %p"))

def ToggleMainHeat():
    
    global MainHeat
    
    if MainHeat == 1:
        MainHeat = 0
        print('MainHeat Off')
    
    else:
        MainHeat = 1
        print('MainHeat On')
        
    
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
    
def on_connect(client, userdata, flags, rc):
     
    client.subscribe(TOGGLE_PATH)
    
def on_message(client, userdata, msg):
       
    Request = str(msg.payload)
  
    if Request[2] == '1':   
        ToggleMainHeat()
        
    elif Request[2] == '2':   
        ToggleBoostHeat()
        
    elif Request[2] == '3':
        ToggleLight()
        
    elif Request[2] == '4':      
        ToggleBlanket()
        
    else:
        PublishtoDevices()
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 15)
client.loop_forever()
