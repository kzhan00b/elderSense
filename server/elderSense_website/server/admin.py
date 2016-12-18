from django.contrib import admin
from .models import Room, PositiveLog, stateFlag

# Register your models here.

admin.site.register(Room)
admin.site.register(PositiveLog)
admin.site.register(stateFlag)