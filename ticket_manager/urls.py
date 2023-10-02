from django.urls import path, include
from .views import *

urlpatterns = [
    path('', view=default_view, name='ticket_man'),
    path('create_ticket/', view=create_ticket, name='create-ticket'),
    path('view_ticket/<int:id>', view=view_ticket, name="view-ticket"),
]