from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import Account

import json
import requests

@csrf_exempt
def login(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    
    try: 
        tempAcc = Account.objects.get(phoneNumber = data["Phone Number"])
        if (tempAcc.password == data["Password"]):
            print("Password is correct!")
            return(HttpResponse("Valid Login"))
        else:
            print("Password is incorrect!")
            return(HttpResponse("Invalid Password"))
        
    except ObjectDoesNotExist:
        print("Account does not exist")
        return(HttpResponse("Invalid Account"))
    

@csrf_exempt
def signup(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    checkHP = data["Phone Number"]
    
    try:
        Account.objects.get(phoneNumber = checkHP)
        print("Same Number exists!")
        return(HttpResponse("Duplicate exists!"))
    
    except ObjectDoesNotExist:
        tempAcc = Account()
        tempAcc.name = data["Name"]
        tempAcc.address = data["Address"]
        tempAcc.phoneNumber = data["Phone Number"]
        tempAcc.password = data["Password"]
        tempAcc.userType = data["User Type"]
        tempAcc.save()
        print("Account with phone number of " + data["Phone Number"] + " has been created.")
        return(HttpResponse("Data received! "))

@csrf_exempt
def registerToken(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    
    print("klasjdfkljasd")
    
    tempData = {
        "dev_id":data["dev_id"],
        "reg_id":data["reg_id"],
        "name":str(Account.objects.get(phoneNumber = data["dev_id"]).name)
    }
    
    print("123123123")
    
    httpRequests = requests.post('http://127.0.0.1:8000/server/fcm/v1/devices/', tempData)
    if (httpRequests.status_code == 201):
                print(httpRequests.text)
    else:   
                print("NAY")
            
    return(HttpResponse("Data received! "))