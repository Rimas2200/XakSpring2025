from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from .app_modules import app_modules_message
class CustomAdminSite(AdminSite):

    def register(self, model_or_iterable, admin_class=None, **options):
        print(f"Регистрация модели: {model_or_iterable}")
        super().register(model_or_iterable, admin_class, **options)
    
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        
        app_list.append(app_modules_message)
        # app_list.sort(reverse=True)
        
        
        
        return app_list
    


# Создаем экземпляр кастомной админки
custom_admin_site = CustomAdminSite() # CustomAdminSite(name='custom_admin')
