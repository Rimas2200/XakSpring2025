from django.db import models

# Create your models here.

class Culture(models.Model):
    Name_of_cultures = models.CharField(max_length=255, verbose_name='Наименование культур')

    class Meta:
        verbose_name = 'Наименование культур'
        verbose_name_plural = 'Наименование культур'
        ordering = ['Name_of_cultures']