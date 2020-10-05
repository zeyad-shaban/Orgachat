import json
from channels.generic.websocket import AsyncWebsocketConsumer


class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = str(self.scope['url_route']['kwargs']['room_id'])
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_layer)

    async def receive(self, text_data):
        message_json = json.loads(text_data)
        await self.channel_layer.group_send(self.group_name, {
            'type': 'send_message',
            'content': message_json['content'],
            'area': message_json['area'],
            'area_id': message_json['area_id'],
            'username': self.scope['user'].username,

        })

    async def send_message(self, event):
        await self.send(json.dumps(event))