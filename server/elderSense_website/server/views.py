#C:\Users\Kzhan00b\Desktop\elderSense.git\trunk\server\elderSense_website

#imports
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import Room, PositiveLog, stateFlag
from datetime import datetime, timedelta
import json
import time

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
    try: 
        tempLog = PositiveLog()
        tempLog.room = Room.objects.get(room=data['room'])
        tempLog.date = data['date']
        tempLog.save()
    
    except ObjectDoesNotExist:
        print("This Room does not exist, contact the administrator! ")
    
    
    #http://stackoverflow.com/questions/291945/how-do-i-filter-foreignkey-choices-in-a-django-modelform
    
    #Select all tuples from PositiveLog which belongs to the specified room
    querySet = PositiveLog.objects.filter(room=data['room'])
    
    return(HttpResponse("The number of entries currently is at: " + str(querySet.count())))
    
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
    if (timeDifference > 15*60):
        
        #Set the datetime object where the threshold time of after 15 minutes where the alert is first flagged to the elder
        #http://stackoverflow.com/questions/18406165/creating-a-timer-in-python
        timeoutThreshold = datetime.now() + timedelta(minutes=1) #timeout = 15 minutes
        
        boolAlertCheck = True
        changeState(boolAlertCheck)
        print("\n\nSound the alarm!!!!\n\n")
        
        while (boolAlertCheck == True):
            #send a http request to the elder's phone, quick http request, then come back immediately
            print("Inside the alert loop now...")
            if (timeoutThreshold < datetime.now()): 
                print("\n\nALERT SENT TO FAMILY NOW\n\n") #keep alerting family? or set some limit? ****
                
                #insert timer here to trigger alert to family
                #put another boolean here to state if alert has been sent to family, if elder replies, need to cascade and tell family that everything is fine.
                pass
                
            boolAlertCheck = stateFlag.objects.get(name="alertState").state
            print(boolAlertCheck)
            time.sleep(5)
            
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
    #
    #Assuming alert sent to elder/family, will need to 
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    
    #request = stateName, deviceName
    changeState(False, data["stateName"])
    return(HttpResponse("Okay state has been changed"))

def changeState(decision, stateName):
    #function to change the state of the alertState flag
    changeState = stateFlag.objects.get(name=stateName)
    changeState.state = decision
    changeState.save()