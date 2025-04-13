# В файле core/custom_admin.py
from django.contrib.admin.sites import AdminSite

class CustomAdminSite(AdminSite):

    def register(self, model_or_iterable, admin_class=None, **options):
        print(f"Регистрация модели: {model_or_iterable}")
        super().register(model_or_iterable, admin_class, **options)
        
    def each_context(self, request):
        context = super().each_context(request)
        context['side_menu'] = [
            {'label': 'Главная Страница', 'url': 'admin:index'},
            {'label': 'Пользователи', 'url': 'auth/user/'},
            {'label': 'Новая Менюшка', 'url': '/admin/custom-menu/'},
        ]
        return context


# Создаем экземпляр кастомной админки
custom_admin_site = CustomAdminSite(name='custom_admin')
