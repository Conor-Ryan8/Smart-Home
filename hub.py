import socket
import time
import threading
import datetime
import Adafruit_DHT
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
from rpi_rf import RFDevice
import requests, json

#Weather API Setup
Key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Openmap = "http://api.openweathermap.org/data/2.5/weather?"
Home = "Limerick"
URL = Openmap + "appid=" + Key + "&q=" + Home

#MQTT Setup
MQTT_SERVER = "x.x.x.x"
DEVICE_PATH = "DEVICES"
TOGGLE_PATH = "Toggle"

Heat = 0
Light = 0
Blanket = 0
InTemp = 0
InHumid = 0
OutTemp = 0
OutHumid = 0
MinTemp = 20

def Timestamp():
    
    timestamp = datetime.datetime.now().strftime("%I:%M%p")
    return timestamp

def ControlSockets():
    
    global Heat
    global Light
    global Blanket
    global InTemp
    global InHumid
    global MinTemp
    
    Radio = RFDevice(17)
    Radio.enable_tx()

    MainHeatOn = 5330227
    MainHeatOff = 5330236
    unusedon = 5332227
    unusedoff = 5332236
    LightOn = 5330691
    LightOff = 5330700
    BlanketOn = 5330371
    BlanketOff = 5330380     
    PIN = 189
        
    while True:
        
        if  Heat == 0 or int(InTemp) > MinTemp:
            
            Radio.tx_code(MainHeatOff, 1, PIN)
        
        elif Heat == 1 and int(InTemp) < MinTemp:
            
            Radio.tx_code(MainHeatOn, 1, PIN)
        
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

def Temperatures():
    
    global InTemp
    global InHumid
    global OutTemp
    global OutHumid
    ExistingWeather = ""
       
    while True:
        
        #Attempt to get data from the sensor module
        H, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22,27)
        
        #Check if data was found
        if T is not None and H is not None:       
            
            #Round it to 1 decimal place
            T = round(T,1)
            H = int(H)
            
            #IF Changed AND between 0-49 AND the first reading
            #OR Changed AND between 0-49 AND not fluctuated more than 10%
            if T!=InTemp and T>=0 and T<50 and InTemp==0 or T!=InTemp and T>=0 and T<50 and T<InTemp*1.1 and T>InTemp*0.9:

                if H!=InHumid and H>=0 and H<=100 and InHumid==0 or H!=InHumid and H>=0 and H<=100 and H<InHumid*1.1 and H>InHumid*0.9:

                    InTemp = T
                    InHumid = H      
                    print(Timestamp()+" - Indoor "+str(T)+"° - "+str(H)+"% Humidity")
                    PublishtoDevices()
                              
        try:
            Response = requests.get(URL)
            Data = Response.json()
            Weather = Data['main']

            if Weather != ExistingWeather:
                        
                OutHumid = Weather['humidity']
                Kelvin = Weather['temp']
                OutTemp = round(Kelvin - 273,1)
                ExistingWeather = Weather
                print(Timestamp()+" - Outdoor - "+str(OutTemp)+"° - "+str(OutHumid)+"% Humidity")
                PublishtoDevices()
                      
        except:
            print(Timestamp()+" - Weather Error")
        
        time.sleep(15)
            
def PublishtoDevices():
    
    global Heat
    global Light
    global Blanket
    global InTemp
    global MinTemp
    
    try:
        
        Data = str(Heat)+","+str(Light)+","+str(Blanket)+","+str(InTemp)+","+str(InHumid)+","+str(OutTemp)+","+str(OutHumid)+","+str(MinTemp)
        publish.single(DEVICE_PATH, Data, hostname=MQTT_SERVER)
    
    except:
        
        print(Timestamp()+' - Error publishing')
        
def ToggleHeat():
    
    global Heat
    
    if Heat == 1:
        
        Heat = 0
        print(Timestamp()+' - Heat Off')
    
    else:
        
        Heat = 1
        print(Timestamp()+' - Heat On')
         
    PublishtoDevices()
               
def ToggleLight():
    
    global Light
    
    if Light == 1:
        
        Light = 0
        print(Timestamp()+' - Light Off')
    
    else:
        
        Light = 1
        print(Timestamp()+' - Light On')
        
    PublishtoDevices()
        
def ToggleBlanket():
    
    global Blanket
    Interupted = 0
       
    if Blanket == 0:
        
        Blanket = 1
        PublishtoDevices()
        print(Timestamp()+' - Blanket On - 30 minutes')   
            
        for Seconds in range (1,18):
            
            if Blanket == 0:
                Interupted = 1
                break            
            else:
                time.sleep(1)
                       
        if Interupted == 0:            
            Blanket = 0        
            PublishtoDevices()
            print(Timestamp()+' - Blanket Auto Off')
            
        else:
            Interupted = 0    
    else:    
        Blanket = 0        
        PublishtoDevices()
        print(Timestamp()+' - Blanket Off') 
    
def ToggleThermostat():

    global MinTemp
    
    if MinTemp is 18:       
        MinTemp = 19
        
    elif MinTemp is 19:        
        MinTemp = 20
        
    elif MinTemp is 20:        
        MinTemp = 21
        
    elif MinTemp is 21:         
        MinTemp = 18
    
    else:
        print('Thermostat setting out of range')
    
    PublishtoDevices()
    print(Timestamp()+' - Thermostat setting - '+str(MinTemp)+'°')
    
    
def on_connect(client, userdata, flags, rc):
     
    client.subscribe(TOGGLE_PATH)
    
def on_message(client, userdata, msg):
       
    Request = str(msg.payload)
  
    if Request[2] == '1':
        
        ToggleHeat()
        
    elif Request[2] == '2':
        
        ToggleLight()
        
    elif Request[2] == '3':
        
        HeatBed = threading.Thread(target=ToggleBlanket)
        HeatBed.start()
        
    elif Request[2] == '4':
        
        ToggleThermostat()
        
    else:
        PublishtoDevices()
 
#start listening and sensor threads
Sockets = threading.Thread(target=ControlSockets)
Devices = threading.Thread(target=PublishtoDevices)
Temps = threading.Thread(target=Temperatures)
Sockets.start()
Devices.start()
Temps.start() 
 
#startup complete status message
print (Timestamp()+" - <<< Raspberry Pi Hub Online >>>")
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 15)
client.loop_forever()
