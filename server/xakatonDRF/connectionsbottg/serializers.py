from rest_framework import serializers
from .models import SavesTgMessages, PhotoMessages

class SaveMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavesTgMessages
        fields = ('sender', 'message', 'userid', 'timestamp', 'chat_id')

        
class PhotoMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoMessages
        fields = ['sender', 'message', 'userid', 'chat_id', 'photo']