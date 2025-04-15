from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_main_menu, name='menu'),  # Главная страница с меню
    path('table/', views.table_menu, name='table_menu'),  # Страница с таблицей
]