from django.forms import model_to_dict
from rest_framework import generics, viewsets, status


from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.


from .models import PhotoMessages, SavesTgMessages
from .serializers import PhotoMessagesSerializer, SaveMessagesSerializer

class SaveMessagesListView(viewsets.ModelViewSet):  
    queryset = SavesTgMessages.objects.all()
    serializer_class = SaveMessagesSerializer

    def post(self, request):
        print(request.data)
        message_save = SavesTgMessages.objects.create(
            sender=request.data['sender'],
            message=request.data["message"],
            userid=request.data['userid'],
            chat_id=request.data["chat_id"],
        )
        
        
        return Response({ 
            "save_message": model_to_dict(message_save)

            }, status=status.HTTP_201_CREATED
            )
        
class PhotoMessagesViewSet(viewsets.ModelViewSet):
    queryset = PhotoMessages.objects.all()
    serializer_class = PhotoMessagesSerializer
    parser_classes = [MultiPartParser, FormParser]  # Для обработки файлов

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
