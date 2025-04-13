from django.contrib import admin
from .models import SavesTgMessages, PhotoTgMessages, SaveMessagesWhatsApp
from custom_admin.custom_admin import custom_admin_site

# Register your models here.



@admin.register(SavesTgMessages, site=custom_admin_site)
class SavesTgMessagesAdmin(admin.ModelAdmin):
    list_display = ('sender', 'message', 'userid', 'timestamp', 'chat_id')
    search_fields = ('sender', 'message', 'userid', 'chat_id')
    list_filter = ('sender', 'timestamp')


@admin.register(PhotoTgMessages, site=custom_admin_site)
class PhotoTgMessagesAdmin(admin.ModelAdmin):
    list_display = ('sender', 'message', 'userid', 'timestamp', 'chat_id', 'photo')
    search_fields = ('sender', 'message', 'userid', 'chat_id')
    list_filter = ('sender', 'timestamp')

@admin.register(SaveMessagesWhatsApp, site=custom_admin_site)
class SaveMessagesWhatsAppAdmin(admin.ModelAdmin):
    list_display = ('sender', 'message', 'userid', 'timestamp', 'chat_id')
    search_fields = ('sender', 'message', 'userid', 'chat_id')
    list_filter = ('sender', 'timestamp')


