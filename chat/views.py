from django.shortcuts import render, get_object_or_404
from support.models import Ticket
from .models import Message

def ticket_chat_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    messages = ticket.messages.order_by('timestamp')
    return render(request, 'chat/chat.html', {
        'ticket': ticket,
        'messages': messages
    })
