from django.urls import path, include
from .views import *

urlpatterns = [
    path('', view=default_view, name='ticket_man'),
]