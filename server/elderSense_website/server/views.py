from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
#from django.utils import simplejson

# Create your views here.
@csrf_exempt
def index(request):
    print(request.scheme + "\n")
    print(str(request.body))
    print(request.GET[room])
    return(HttpResponse("Input received! "))