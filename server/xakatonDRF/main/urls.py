from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_main_menu, name='menu'),
    path('table_clear/', views.table_menu, name='table_menu'),
    path('model_menu/', views.models_menu, name='model_menu'),
    path('process/telegram', views.process_telegram, name='process_telegram'),
    path('process/whatsapp', views.process_whatsapp, name='process_whatsapp'),

]