from django.urls import path, include
from .views import *

urlpatterns = [
    path('', view=default_view, name='ticket_man'),
    path('create_ticket/', view=create_ticket, name='create-ticket'),
    path('view_ticket/<int:id>', view=view_ticket, name="view-ticket"),
    path('close_task/<int:id>', view=close_task, name='close-task'),
    path('close_ticket/<int:id>', view=close_ticket, name='close-ticket'),
    path('re_open_task/<int:id>', view=re_open_task, name='re-open-task'),
    path('create_task/<int:ticket_id>', view=create_task_form, name='create-task-form'),
    path('create_task/', view=create_task, name='create-task'),
    path('reassign_ticket/', view=re_assign_ticket, name='re-assign-ticket'),
    path('delete_task/<int:task_id>', view=delete_task, name='delete-task'),
]