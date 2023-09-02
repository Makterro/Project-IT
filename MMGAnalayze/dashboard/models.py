from django.db import models
from analyzeDashboard.models import Building


# Create your models here.
class CompanySensor(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    telephone = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Sensor(models.Model):
    model = models.CharField(max_length=100, blank=False, null=False)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    manufacturer = models.ForeignKey(CompanySensor, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.model


class SensorReading(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно считано'),
        ('problem', 'Возникли проблемы'),
        ('critical', 'Критическое значение')
    ]

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='success')
    build = models.ForeignKey(Building, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)  # допустим - "Датчик работает штатно." "Обнаружена проблема!"
    timestamp = models.DateTimeField(auto_now_add=True)  # время сбора данных
    datetime = models.DateTimeField(null=True, blank=True) #Время ДЛЯ ПРОВЕРКИ РАБОТЫ

    air_temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # температура воздуха
    surface_soil_temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True,
                                                   null=True)  # температура грунта на поверхности
    soil_temperature_5m = models.DecimalField(max_digits=5, decimal_places=2, blank=True,
                                              null=True)  # температура грунта на глубине 5 метров
    soil_temperature_10m = models.DecimalField(max_digits=5, decimal_places=2, blank=True,
                                               null=True)  # температура грунта на глубине 10 метров

    def __str__(self):
        return f"{self.sensor} - {self.timestamp} - {self.description}"
