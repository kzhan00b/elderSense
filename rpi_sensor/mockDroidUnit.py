import requests
import json
from datetime import datetime
#from PIR_Test import myconverter

data = {
    "deviceName" : "elderPhone",
    "stateName" : "processState",
}

r = requests.get('http://127.0.0.1:8000/server/ssProcessing/', json.dumps(data))
#r = requests.post('http://127.0.0.1:8000/server/androidResponse/', json.dumps(data))