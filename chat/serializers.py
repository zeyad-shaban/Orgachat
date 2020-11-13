from chat.models import Chat
from rest_framework.serializers import ModelSerializer

class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'