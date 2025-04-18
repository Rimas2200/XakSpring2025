from django.contrib import admin
from .models import Culture
from custom_admin.custom_admin import custom_admin_site
# Register your models here.


@admin.register(Culture, site=custom_admin_site)
class CultureAdmin(admin.ModelAdmin):
    list_display = ('id', 'Name_of_cultures')
    search_fields = ('Name_of_cultures',)
    list_filter = ('Name_of_cultures',)