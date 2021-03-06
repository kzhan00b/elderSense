#C:\Users\Kzhan00b\Desktop\elderSense.git\trunk\server\elderSense_website

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from fcm.utils import get_device_model

from .models import Room, PositiveLog, stateFlag, Account
from datetime import datetime, timedelta

import json
import time
import requests

#Start of code
@csrf_exempt
def index(request):
    #debug lines
    #print(request.scheme + "\n")
    #print(str(request.body)  + "\n")
    
    #http://stackoverflow.com/questions/29780060/trying-to-parse-request-body-from-post-in-django
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    
    #insert data into database
    insertLog(data["room"])
    #Check if alert state is true, if yes, put to false as elder is moving around
    boolAlertCheck = stateFlag.objects.get(name="alertState")
    if (boolAlertCheck.state == True):
        changeState(False, "alertState")
        disableAlerts()
    
    #http://stackoverflow.com/questions/291945/how-do-i-filter-foreignkey-choices-in-a-django-modelform
    #Select all tuples from PositiveLog which belongs to the specified room
    querySet = PositiveLog.objects.filter(room=data['room'])
    
    return(HttpResponse("The number of entries currently is at: " + str(querySet.count())))

def insertLog(roomName):
    try:
        tempLog = PositiveLog()
        tempLog.room = Room.objects.get(room=roomName)
        tempLog.date = datetime.now()
        print(str(datetime.now()))
        tempLog.save()
        return True

    except ObjectDoesNotExist:
        #Maybe put some way to log this issue? 
        print("This Room does not exist, contact the administrator! ")
        return False

def ssProcessing(request):
    changeState(True, "processState")
    boolCheck = stateFlag.objects.get(name="processState").state
    
    while (boolCheck == True):
        print("Internal server processing here...")
        
        #periodically check if alert needs to be sounded
        inactivityMonitor()
        
        #querySet = PositiveLog.objects.filter(room='Living Room')
        #print("There are " + str( querySet.count() ) + " number of entries now!")
        time.sleep(10)
        boolCheck = stateFlag.objects.get(name="processState").state

    print("Waking this process now!")
    return(HttpResponse())



    
def inactivityMonitor():
    '''
    Track for basic inactivity within the house
    Assume threshold to be 30 minutes 
    Sound the alarm if inactive
    
    https://docs.djangoproject.com/en/dev/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    *incase required to order the list of positiveLogs*
    '''  
    
    currentTime = datetime.now()
    #http://stackoverflow.com/questions/6685834/django-want-to-sort-comments-by-datetime
    lastLog = PositiveLog.objects.latest('date')
    
    #http://stackoverflow.com/questions/1345827/how-do-i-find-the-time-difference-between-two-datetime-objects-in-python
    #http://stackoverflow.com/questions/20631855/get-the-difference-between-two-datetime-objects-in-minutes-in-python
    timeDifference = (currentTime - lastLog.date).total_seconds()
    if (timeDifference > 1*60):
        
        #Set the datetime object where the threshold time of after 15 minutes where the alert is first flagged to the elder
        #http://stackoverflow.com/questions/18406165/creating-a-timer-in-python
        timeoutThreshold = datetime.now() + timedelta(minutes=1) #timeout = 15 minutes

        #send alert and set elderAlert flag to True
        print("Alert to be sent to elder's phone")
        tempAccount = Account.objects.get(userType = "Elder")
        phoneNumber = tempAccount.phoneNumber
        
        
        #tempDevice = MyDevice.objects.get(dev_id = phoneNumber, name = tempAccount.name)
        #regID = tempDevice.reg_id
        
        Device = get_device_model()
        my_phone = Device.objects.get(dev_id = phoneNumber)
        my_phone.send_message({
            'message':'my test message'
        })
        
        '''
        print(regID)
        test = {"to":regID}
        message = {
            'to':regID,
            'notification':{
                'title':'Inactivity Detected!',
                'body':'Please move around house or deactivate alert through phone!'
            },
            'priority': 'high'
        }
        
        r = requests.post('https://fcm.googleapis.com/fcm/send', 
                      data=json.dumps(test),
                      headers = {
                          'Authorization': 'key=AAAA4Rk__ek:APA91bEqZTWrNIRHXNTT8nse4yD6XSKNXalbsM46phizb-I3ZGxyzbAmVREVSyuBOBY_b_uOZtgiFZnb89_BRgXIeARrRv4vxNL5JJlgHPE0khJqOV0TWWI8C6oasZGtOLHvh_nrgB8Y',
                          'Content-Type': 'application/json',
                      }
                     )
        
        print(r.status_code)
        print(r.text)
        '''
        
        tempState = stateFlag.objects.get(name="elderPhoneAlertState")
        tempState.state = True
        tempState.save()

        boolAlertCheck = True
        changeState(boolAlertCheck, "alertState")
        
        while (boolAlertCheck == True):
            print("Inside the alert loop now...")
            tempState = stateFlag.objects.get(name="familyPhoneAlertState")

            if (timeoutThreshold < datetime.now() and not tempState.state):
                print("\n\nALERT SENT TO FAMILY NOW\n\n") #keep alerting family? or set some limit? ****
                tempState.state = True
                tempState.save()
                
            time.sleep(5)
            boolAlertCheck = stateFlag.objects.get(name="alertState").state
    #print("Current time now is: " + currentTime.strftime("%c"))

    
def computeTrend(request):
    '''
    http://stackoverflow.com/questions/12851208/how-to-detect-significant-change-trend-in-a-time-series-data
    http://stackoverflow.com/questions/12851208/how-to-detect-significant-change-trend-in-a-time-series-data/12874212#12874212
    http://blog.thomnichols.org/2011/08/smoothing-sensor-data-with-a-low-pass-filter
    use low pass filter...? 
    '''
    pass

@csrf_exempt
def androidResponse(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    
    #request = stateName, deviceName
    changeState(False, data["stateName"])
    r = insertLog(data["deviceName"])
    if (r == False):
        print("Log not stored, Error.")

    disableAlerts()
    return(HttpResponse("Okay state has been changed"))

def disableAlerts():
    #need to return? KIV 
    tempState = stateFlag.objects.get(name="familyPhoneAlertState")
    if (tempState.state == True):
        print("http request sent to familyPhone to notify/update that elder is ok")
        tempState.state = False
        tempState.save()
    tempState = stateFlag.objects.get(name="elderPhoneAlertState")
    if (tempState.state == True):
        tempState.state = False
        tempState.save()

def changeState(decision, stateName):
    #function to change the state of the alertState flag
    changeState = stateFlag.objects.get(name=stateName)
    changeState.state = decision
    changeState.save()