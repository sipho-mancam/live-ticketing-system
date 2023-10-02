from django.urls import path, include 
from .views import *


urlpatterns = [
    path('', view=index, name="index"),   
    path('accounts/profile/', view=profile, name='signed_in'),
    path('ticket_man/', include('ticket_manager.urls'), name="ticket_man"),
]