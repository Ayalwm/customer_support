from django.urls import path
from . import views

urlpatterns = [
    path('tickets/<int:ticket_id>/chat/', views.ticket_chat_view, name='ticket_chat'),
]
