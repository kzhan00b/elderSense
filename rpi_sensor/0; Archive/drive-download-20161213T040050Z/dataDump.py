from datetime import datetime

def dataDump():
    year = 2016
    month = 12
    day = 12
    
    hour = 0
    minute = 0
    seconds = 0
    milliseconds = 0
    
    while (hour != 6):
        mockTime = datetime(
            year, month, day,
            hour, minute, seconds,
            milliseconds
        )
        sensorActivate_log("Bedroom", mockTime)
        hour += 1
        
    while (hour != 8):
        mockTime = datetime(
            year, month, day,
            hour, minute, seconds,
            milliseconds
        )
        sensorActivate_log("Kitchen", mockTime)
        hour += 1
        
    while (hour != 12):
        mockTime = datetime(
            year, month, day,
            hour, minute, seconds,
            milliseconds
        )
        sensorActivate_log("Living Room", mockTime)
        hour += 1
    
    while (hour != 18):
        mockTime = datetime(
            year, month, day,
            hour, minute, seconds,
            milliseconds
        )
        sensorActivate_log("Bedroom", mockTime)
        hour += 1
    
    while (hour != 24):
        mockTime = datetime(
            year, month, day,
            hour, minute, seconds,
            milliseconds
        )
        sensorActivate_log("Living Room", mockTime)
        hour += 1
        
