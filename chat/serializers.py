from chat.models import Chat, Message
from rest_framework.serializers import ModelSerializer

class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'