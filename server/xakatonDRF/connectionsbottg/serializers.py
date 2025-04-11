from rest_framework import serializers
from .models import SavesTgMessages

class SaveMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavesTgMessages
        fields = ('sender', 'message', 'userid', 'timestamp', 'chat_id')

        
        
        
        