#C:\Users\Kzhan00b\Desktop\elderSense.git\trunk\server\elderSense_website

#imports
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import Room, PositiveLog
import json

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
    #return(HttpResponse("Input received! "))