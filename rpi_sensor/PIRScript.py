import RPi.GPIO as GPIO
import time
import json
import logging
import requests
from datetime import datetime

global roomName
roomName = 'Living Room'

logging.basicConfig(filename = 'timelog.log', level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt = '%m/%d/%Y %I:%M:%S %p')

def sensorActivate_log(currentTime):
    
    data = {
        "room" : roomName,
        "date" : currentTime,        
    }
    
    r = requests.post('http://127.0.0.1:8000/server/',
                     json.dumps(data, default = myconverter))
    
    if (r.status_code == 200):
        print(r.text)
        logging.warning(': ' + roomName)
    else:
        logging.warning(': Error sending data to server!')
        
        
def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()
    
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(14, GPIO.IN)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.IN)
    
while True:
    #Set s1/s2 to sensor output [1 OR 0]
    s1 = GPIO.input(14)
    s2 = GPIO.input(15)
    
    #If both sensors detect movement
    if s1 and s2 is 1:
        
        #Check 5 times within 1 second
        for check in range(5):
            #Take sensor output again
            s1 = GPIO.input(14)
            s2 = GPIO.input(15)
            
            if s1 and s2 is 0:
                #Check to ensure not ghost readings
                break
            
            #sleep .2 seconds before taking next sample
            time.sleep(.2)
        
        if check is 5:
            #Movement detected, send to server
            sensorActivate_log(datetime.now())
        