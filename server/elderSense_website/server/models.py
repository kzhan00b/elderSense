from django.db import models
from datetime import datetime

# Create your models here.

class Room(models.Model):
    
    room = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.room
    
class PositiveLog(models.Model):
    
    room = models.ForeignKey(
        Room, on_delete = models.CASCADE,
    )
    
    date = models.DateTimeField()
    
    def __str__(self):
        #return str(type(self.date))
        return self.date.strftime("%c")
    