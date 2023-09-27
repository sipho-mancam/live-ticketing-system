from django.urls import path, include 
from .views import *


urlpatterns = [
    path('', view=index, name="index-page"),   
    path('accounts/profile/', view=profile) 
]