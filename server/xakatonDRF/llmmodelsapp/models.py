from django.db import models

# Create your models here.

class WhatsAppChat(models.Model):
    chat_name = models.CharField(max_length=255)
    chat_id = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.chat_name
    
    class Meta:
        verbose_name = 'Чат WhatsApp'
        verbose_name_plural = 'Чаты WhatsApp'
    
