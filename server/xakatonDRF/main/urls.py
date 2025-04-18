from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_main_menu, name='menu'),
    path('table_clear/', views.table_menu, name='table_menu'),
    path('model_menu/', views.models_menu, name='model_menu'),
    path('process_telegram/', views.correct_loading_date_tg, name='process_telegram'),
    path('process_whatsapp/', views.correct_loading_date_whatsapp, name='process_whatsapp'),
    path('load_data_to_table/', views.load_data_to_table, name='load_data_to_table'),
]