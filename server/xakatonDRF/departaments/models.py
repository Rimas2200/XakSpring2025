from django.db import models

# Create your models here.

class DepartmentProduction(models.Model):
    Division = models.CharField(max_length=255, verbose_name='Наименование подразделения')
    Production_site = models.CharField(max_length=255, verbose_name='Наименование производственного участка')
    Branch_number = models.CharField(max_length=255, verbose_name='Номер филиала')
    

    class Meta:
        verbose_name = 'Принадлежность отделений и производственных участков (ПУ) к подразделениям'
