from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('main.urls')),  # Подключаем главную страницу
    path('admin/', include('custom_admin.urls')),  # Подключаем кастомную админку
    path('api/v1/', include('connectionsbottg.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
