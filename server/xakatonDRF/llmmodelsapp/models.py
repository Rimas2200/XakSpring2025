from django.db import models
from connectionsbottg.models import SavesTgMessages, SaveMessagesWhatsApp
# Create your models here.

class WhatsAppChat(models.Model):
    chat_name = models.CharField(max_length=255, verbose_name='Название чата')
    chat_id = models.CharField(max_length=255, unique=True, verbose_name='ID чата')
    # WhatsApp or Telegram
    chat_type = models.CharField(max_length=50, verbose_name='Тип чата')
    # created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    def __str__(self):
        return self.chat_name
    
    class Meta:
        verbose_name = 'Чат WhatsApp'
        verbose_name_plural = 'Чаты WhatsApp'
        
class ProcessedMessagesTelegramm(models.Model):
    chat_id = models.CharField(max_length=255, verbose_name='ID чата')
    Message = models.ForeignKey(SavesTgMessages, on_delete=models.CASCADE)
    processed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата обработки')
    
    def __str__(self):
        return f"Message {self.message_id} in {self.chat.chat_name}"
    
    class Meta:
        verbose_name = 'Обработанное сообщение'
        verbose_name_plural = 'Обработанные сообщения' 

class ProcessedMessagesWhatsApp(models.Model):
    chat = models.ForeignKey(WhatsAppChat, on_delete=models.CASCADE, verbose_name='Чат')
    Message = models.ForeignKey(SaveMessagesWhatsApp, on_delete=models.CASCADE)
    processed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата обработки')
    
    def __str__(self):
        return f"Message {self.message_id} in {self.chat.chat_name}"
    
    class Meta:
        verbose_name = 'Обработанное сообщение WhatsApp'
        verbose_name_plural = 'Обработанные сообщения WhatsApp'
