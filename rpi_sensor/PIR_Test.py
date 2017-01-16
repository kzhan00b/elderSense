#C:\Users\Kzhan00b\Desktop\elderSense.git\trunk\rpi_sensor

#import RPi.GPIO as GPIO
import time
import json
import logging
import requests
#from dataDump import dataDump
from datetime import datetime

#dataDump()

logging.basicConfig(filename = 'example.log', level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt = '%m/%d/%Y %I:%M:%S %p')

def sensorActivate_log(specifiedRoom, mockTime):
        logging.warning(': Living Room')
        
        data = {
            "room" : specifiedRoom,
            "date" : mockTime,
            #"date" : datetime.now()
        }
        
        httpRequests = requests.post('http://127.0.0.1:8000/server/', json.dumps(data, default = myconverter))

        if (httpRequests.status_code == 200):
                print(httpRequests.text)
        else:   
                print("NAY")

def myconverter(o):
    #https://code-maven.com/serialize-datetime-object-as-json-in-python
    if isinstance(o, datetime):
        return o.__str__()        

for i in range(10):
    sensorActivate_log("Living Room1", datetime.now())
    time.sleep(3) 

    
'''
a=0
while a <10:
       ticks = time.time()
       print ("Number of ticks since 12:00am, January 1, 1970: ", ticks)
       a += 1

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN)

while True:
       i=GPIO.input(10)
       if i==0:                 #When output from motion sensor is LOW
             print ("No intruders",i)
             time.sleep(0.1)
             
       elif i==1:               #When output from motion sensor is HIGH
             print ("AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH\n\n")
             time.sleep(0.1)
'''


def dataDump():
    year = 2016
    month = 12
    day = 12
    
    hour = 0
    minute = 0
    seconds = 0
    milliseconds = 0
    
    while (hour != 6):
        mockTime = datetime(
            year, month, day,
            hour, minute, seconds,
            milliseconds
        )
        sensorActivate_log("Bedroom", mockTime)
        hour += 1
        
    while (hour != 8):
        mockTime = datetime(
            year, month, day,
            hour, minute, seconds,
            milliseconds
        )
        sensorActivate_log("Kitchen", mockTime)
        hour += 1
        
    while (hour != 12):
        mockTime = datetime(
            year, month, day,
            hour, minute, seconds,
            milliseconds
        )
        sensorActivate_log("Living Room", mockTime)
        hour += 1
    
    while (hour != 18):
        mockTime = datetime(
            year, month, day,
            hour, minute, seconds,
            milliseconds
        )
        sensorActivate_log("Bedroom", mockTime)
        hour += 1
    
    while (hour != 24):
        mockTime = datetime(
            year, month, day,
            hour, minute, seconds,
            milliseconds
        )
        sensorActivate_log("Living Room", mockTime)
        hour += 1
        
