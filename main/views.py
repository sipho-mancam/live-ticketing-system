from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from pprint import pprint
# Create your views here.
from allauth.account.signals import user_logged_in, user_logged_out, user_signed_up
from django.dispatch import receiver

# Define the receiver function
@receiver(user_logged_in)
def user_logged_in_handler(sender, request:HttpRequest, user, **kwargs):
    # Your logic for when a user logs in
    pass
    # Additional actions based on the login

@receiver(user_logged_out)
def user_logged_out_handler(sender, request:HttpRequest, user, **kwargs):
    pass



def index(request:HttpRequest)->HttpResponse:
    return render(request, 'index.html', {})

def profile(request:HttpRequest)->HttpResponse:
    return index(request)