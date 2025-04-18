from django.contrib import admin
#from custom_admin.custom_admin import custom_admin_site
from .models import Operation
# Register your models here.

@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('Names_of_field_work', 'Note')
    search_fields = ('Names_of_field_work', 'Note')
    list_filter = ('Names_of_field_work', 'Note')