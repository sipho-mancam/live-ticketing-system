from django.urls import path, include 
from .views import *


urlpatterns = [
    path('', view=index, name="index-page"),   
    path('accounts/profile/', view=profile),
    path('ticket_man/', include('ticket_manager.urls'), name="ticket_man"),
]