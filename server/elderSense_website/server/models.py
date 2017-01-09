from django.conf import settings
from django.db import models
from datetime import datetime
from fcm.models import AbstractDevice

# Create your models here.

class stateFlag(models.Model):
    name = models.CharField(max_length = 100, primary_key=True, default = "alertState")
    state = models.BooleanField(default = False)
    
    def __str__(self):
        return (self.name)
    
class Room(models.Model):
    
    room = models.CharField(max_length = 100, primary_key=True)
    
    def __str__(self):
        return self.room
    
class PositiveLog(models.Model):
    
    room = models.ForeignKey(
        Room, on_delete = models.CASCADE,
    )
    
    date = models.DateTimeField(primary_key=True)
    
    def __str__(self):
        #return str(type(self.date))
        return self.date.strftime("%c")
    
class Account(models.Model):
    name = models.CharField(max_length = 100)
    address = models.CharField(max_length = 200)
    phoneNumber = models.CharField(max_length = 8, primary_key=True)
    password = models.CharField(max_length = 20)
    userType = models.CharField(max_length = 10)
    
    def __str__(self):
        return self.phoneNumber
    
class MyDevice(AbstractDevice):
    #http://stackoverflow.com/questions/14663523/foreign-key-django-model
    #user = models.ForeignKey(settings.AUTH_USER_MODEL)
    '''phoneNumber = models.ForeignKey(
        Account, on_delete = models.CASCADE
    )'''
    pass