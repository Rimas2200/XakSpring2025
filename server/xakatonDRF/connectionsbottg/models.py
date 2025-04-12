from django.db import models

# Create your models here.

class SavesTgMessages(models.Model):

    sender = models.CharField(max_length=255,verbose_name='Отправитель')
    message = models.TextField(verbose_name='Сообщение')
    userid = models.CharField(max_length=255, verbose_name='ID пользователя')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время отправки')
    chat_id = models.CharField(max_length=255, verbose_name='ID чата')


    class Meta:
        verbose_name = 'Сообщения'
        verbose_name_plural = 'Messages'