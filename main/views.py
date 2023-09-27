from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
# Create your views here.


def index(request:HttpRequest)->HttpResponse:

    return HttpResponse("Welcome to the app")

def profile(request:HttpRequest)->HttpResponse:
    
    print(request.headers)
    return HttpResponse(request.headers)