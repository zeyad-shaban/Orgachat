from base64 import b64decode
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from django.shortcuts import get_object_or_404
from .models import Channel, Message, Chat
from django.contrib.auth import get_user_model
User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_name = str(self.scope['url_route']['kwargs']['id'])
        self.userId = self.scope['query_string'][len('userId='):]
        self.user = await sync_to_async(User.objects.get)(id=self.userId)
        await self.channel_layer.group_add(
            self.chat_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.chat_name,
            self.channel_name
        )

    async def receive(self, text_data):
        json_data = json.loads(text_data)
        chat = await sync_to_async(get_object_or_404)(Chat, pk=int(self.chat_name))
        if chat.type == 'group':
            try:
                channel = await sync_to_async(Channel.objects.get)(id=int(json_data['channelId']))
            except:
                try:
                    channel = await sync_to_async(chat.channel_set.first)()
                except:
                    channel = None
        else:
            channel = None

        if json_data.get('text'):
            message = await sync_to_async(Message.objects.create)(user=self.user, chat=chat, channel=channel, text=json_data.get('text'))
            await sync_to_async(message.save)()
            message = message.to_json()
        else:
            try:
                message = await sync_to_async(Message.objects.get)(id=json_data.get('message')['id'])
                message = await sync_to_async(message.to_json)()
            except:
                return

        await self.channel_layer.group_send(
            self.chat_name,
            {
                'type': 'send_message',
                'message': message
            }
        )

    async def send_message(self, event):
        message = event['message']
        await self.send(json.dumps({
            'message': message
        }))
