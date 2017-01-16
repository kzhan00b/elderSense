import requests
import json

#r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
r = requests.get('http://httpbin.org/get')

'''
#r = requests.get('http://192.168.0.102:8080')
#print(r)#

employees = {}
namelist = []

employees = {"employees" : namelist}
employees["employees"].append({"firstName":"John", "lastName":"Doe"})
employees["employees"].append({"firstName":"Anna", "lastName":"Smith"})
employees["employees"].append({"firstName":"Peter", "lastName":"Jones"})

#jsonObject = json.loads(data)
dataFile = json.dumps(employees)

r = requests.post('http://192.168.0.102:8080', data=dataFile)
print(r)
print(r.json)

#file = open("dumpfile.txt", "w")
#file.write(dumpFile)
#file.close()
#print(jsonObject)


#result = data["markers"]

'''

