from django.urls import path
from . import views
from .custom_admin import custom_admin_site

urlpatterns = [
    
    path('custom-menu/', views.custom_menu_view, name='custom_menu'),
    path('custom-menu/submenu-1/', views.submenu_1_view, name='submenu_1'),
    path('custom-menu/submenu-2/', views.submenu_2_view, name='submenu_2'),

    path('', custom_admin_site.urls),  # Маршруты для кастомной админки
]
