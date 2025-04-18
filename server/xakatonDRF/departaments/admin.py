# В файле admin.py вашего приложения (например, departaments/admin.py)
from django.contrib import admin
from .models import DepartmentProduction
from custom_admin.custom_admin import custom_admin_site


@admin.register(DepartmentProduction, site=custom_admin_site)
class DepartmentProductionAdmin(admin.ModelAdmin):
    list_display = ('id', 'Division', 'Production_site', 'Branch_number')
    search_fields = ('Division', 'Production_site', 'Branch_number')
    list_filter = ('Division', 'Production_site', 'Branch_number')
    