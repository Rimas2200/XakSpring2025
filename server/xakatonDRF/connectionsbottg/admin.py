from django.contrib import admin
from .models import SavesTgMessages, PhotoMessages

# Register your models here.

admin.site.register(SavesTgMessages)
admin.site.register(PhotoMessages)