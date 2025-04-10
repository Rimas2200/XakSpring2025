from django.db import models

# Create your models here.


class Operation(models.Model):
    Names_of_field_work = models.CharField(max_length=255, verbose_name='Наименование полевых работ')
    Note = models.CharField(max_length=255, verbose_name='Примечание')

    class Meta:
        verbose_name = 'Названия операций'
        verbose_name_plural = 'Названия операций'
        ordering = ['Names_of_field_work']