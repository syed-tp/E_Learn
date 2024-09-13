import json
from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async

from channels.db import database_sync_to_async

from django.utils import timezone
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = 'chat_%s' % self.id
        # join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        #accept connetion
        await self.accept()

        #send previous messages
        messages = await self.get_previous_messages()

        for message in messages:
            await self.send(text_data=json.dumps({
                'message': message['content'],
                'user': message['user__username'],
                'datetime': message['timestamp'].isoformat(),
                'id':message['id'],
                
        }))
    
    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
    
    async def receive(self, text_data):
        
        data= json.loads(text_data)
        action = data.get('action', 'send') 

        if action=='send':
            await self.handle_new_message(data['message'])
        
        if action=='delete':
            await self.handle_delete(data['message_id'])

    async def handle_new_message(self, message):
        now = timezone.now()
        message_instance= await self.save_message(self.user, message, self.id)
        # print(f"New message saved with ID: {message_instance.id}")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                   
                'type': 'chat_message',
                'message': message,
                'user':self.user.name,
                'datetime': now.isoformat(),
                'id': message_instance.id,
                'action':'send', 
                
            }
        )

    async def handle_delete(self, message_id):
        print(message_id)
        
        try:
            
            message_id = int(message_id)  # Ensure message_id is an integer
            await self.soft_delete_messages(self.user, message_id)
        

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'user':self.user.username,
                    'message':'This message was deleted.',
                    'datetime': (timezone.now()).isoformat(),
                    'type': 'chat_message',
                    'action': 'delete',
                    'id': message_id,
                }
            )
            print(f"deleted")
        except ValueError:
            print(f"Invalid message_id: {message_id}")


    # receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))


    @database_sync_to_async
    def save_message(self, user, content, course_id):
        # Save the message to the database
        return Message.objects.create(user=user, content=content, course_id=course_id)
    
    @database_sync_to_async
    def soft_delete_messages(self, user, message_id):
        message = Message.objects.filter(id=message_id, user=user).first()
        
        if message:
            message.deleted = True
            message.save()
            
    @database_sync_to_async
    def get_previous_messages(self):
        # Fetch previous messages for this course
        return list(Message.objects.filter(course_id=self.id, deleted = False).order_by('timestamp')[:50].values('id', 'user__username', 'content', 'timestamp'))
    
    