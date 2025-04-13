from django.contrib import admin
from .models import SavesTgMessages, PhotoTgMessages, SaveMessagesWhatsApp

# Register your models here.

admin.site.register(SavesTgMessages)
admin.site.register(PhotoTgMessages)
admin.site.register(SaveMessagesWhatsApp)

