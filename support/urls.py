from django.urls import path

from customer_support import views
from .views import ticket_comment, ticket_list, create_ticket, update_ticket_status

urlpatterns = [
    path('', ticket_list, name='ticket_list'),
    path('new/', create_ticket, name='create_ticket'),
    
    path('<int:ticket_id>/update/', update_ticket_status, name='update_ticket_status'),
    path('<int:ticket_id>/comment', ticket_comment, name='ticket_comment'),


]