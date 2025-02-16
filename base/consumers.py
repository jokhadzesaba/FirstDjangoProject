import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Room, User
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        print(f"Client connected to room {self.room_id}")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print(f"Client disconnected from room {self.room_id}")
        await self.channel_layer.group_discard(
        self.room_group_name,
        self.channel_name
    )
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        email = data['email']
        room = await sync_to_async(Room.objects.get)(id=self.room_id)
        user = await sync_to_async(User.objects.get)(email=email)
        print(f"Received message from {email} in room {self.room_id}: {message}")

        # Save message in the database
        await sync_to_async(Message.objects.create)(
            user=user,
            room=room,
            body=message
        )

        # Send message to the room group
        print(f"Broadcasting message to group {self.room_group_name}")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'email': email
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'email': event['email']
        }))
