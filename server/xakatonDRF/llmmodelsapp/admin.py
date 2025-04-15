from django.contrib import admin

from .models import WhatsAppChat
from custom_admin.custom_admin import custom_admin_site
# Register your models here.

@admin.register(WhatsAppChat, site=custom_admin_site)
class WhatsAppChatAdmin(admin.ModelAdmin):
    list_display = ('chat_name', 'chat_id')
    
