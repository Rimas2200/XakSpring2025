from rest_framework import serializers
from .models import SavesTgMessages, PhotoTgMessages

class SaveMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavesTgMessages
        fields = ('sender', 'message', 'userid', 'timestamp', 'chat_id')

        
class PhotoMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoTgMessages
        fields = ['sender', 'message', 'userid', 'chat_id', 'photo']

class SaveMessagesWhatsAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavesTgMessages
        fields = ('sender', 'message', 'userid', 'timestamp', 'chat_id')