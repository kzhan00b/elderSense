#import RPi.GPIO as GPIO
import time
import json
import logging
import requests
from datetime import datetime


logging.basicConfig(filename = 'example.log', level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt = '%m/%d/%Y %I:%M:%S %p')

def sensorActivate_log():
        logging.warning(': Living Room')
        
        data = {
            "room" : "Living Room",
            "date" : datetime.now()
        }
        
        httpRequests1 = requests.get('http://127.0.0.1:8000/server/', "testing testing 123")
        
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
    sensorActivate_log()
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
