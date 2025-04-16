from django.db import models

# Create your models here.

class ProcessedMessage(models.Model):
    """
    Модель для хранения обработанных сообщений.
    """
    DATE=        models.DateField()
    DEPARTMENT=  models.CharField(max_length=255)  # Подразделение SUBUNIT
    OPERATION=   models.CharField(max_length=255)
    CROP=        models.CharField(max_length=255)
    HECTARE=     models.CharField(max_length=255)  # За день, га
    DAY_YIELD=   models.CharField(max_length=255)  # Вал за день, ц
    YIELD_TOTAL= models.CharField(max_length=255)  # Вал с начала, ц

    