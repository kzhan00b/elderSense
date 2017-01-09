from django.contrib import admin
from .models import Room, PositiveLog, stateFlag, Account

# Register your models here.

admin.site.register(Room)
admin.site.register(PositiveLog)
admin.site.register(stateFlag)
admin.site.register(Account)