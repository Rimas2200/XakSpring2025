from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_main_menu, name='menu'),  # Главная страница с меню
    path('table/', views.table_menu, name='table_menu'),  # Страница с таблицей
    path('model_tables/', views.model_tables, name='model_tables'),  # Страница с таблицами
]