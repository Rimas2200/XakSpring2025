from django.urls import path, include
from rest_framework import routers

from .views import SaveMessagesListView
router = routers.DefaultRouter()

router.register(r'save_messages', SaveMessagesListView, basename='save_messages')

urlpatterns = [
    path('', include(router.urls)),
]

