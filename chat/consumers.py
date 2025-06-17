import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ticket_id = self.scope['url_route']['kwargs']['ticket_id']
        self.room_group_name = f'chat_{self.ticket_id}'
        self.user = self.scope['user']

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data['message']
            
            # Save message and get read status
            message_id = await self.save_message(message)
            
            # Send message to group with read status
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': self.user.username,
                    'message_id': message_id,
                    'timestamp': timezone.now().isoformat(),
                    'read': False  # Messages start unread
                }
            )
            
        except Exception as e:
            print("Error:", e)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender': event['sender'],
            'message_id': event['message_id'],
            'timestamp': event['timestamp'],
            'read': event['read']
        }))

    @sync_to_async
    def save_message(self, message_content):
        from .models import Message, Ticket
        ticket = Ticket.objects.get(id=self.ticket_id)
        message = Message.objects.create(
            ticket=ticket,
            sender=self.user,
            content=message_content
        )
        return message.id