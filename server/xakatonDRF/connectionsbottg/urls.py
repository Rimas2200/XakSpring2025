from django.urls import path, include
from rest_framework import routers

from .views import SaveMessagesListView, PhotoMessagesViewSet
router = routers.DefaultRouter()

router.register(r'save_messages', SaveMessagesListView, basename='save_messages')
router.register(r'save_photo', PhotoMessagesViewSet, basename='save_photo')
router.register(r'save_messages_whatsapp', SaveMessagesListView, basename='save_messages_whatsapp')

urlpatterns = [
    path('', include(router.urls)),
]

