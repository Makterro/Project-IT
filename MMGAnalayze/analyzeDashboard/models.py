from django.contrib.auth.models import User
from django.db import models

from company.models import Company


class Building(models.Model):
    STATUS_CHOICES = [
        ('green', 'Green'),
        ('red', 'Red'),
        ('yellow', 'Yellow'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='green')
    name = models.CharField(max_length=100, blank=False, null=False)
    telephone = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    id_region = models.IntegerField(blank=True, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, blank=False, null=False,
                                on_delete=models.CASCADE, default=0)

    view_image = models.ImageField(upload_to='building_images/', blank=True, null=True)
    condition_image = models.ImageField(upload_to='building_images/', blank=True, null=True)
    frozen_water_amount_image = models.ImageField(upload_to='building_images/', blank=True, null=True)
    scheme_image = models.ImageField(upload_to='building_images/', blank=True, null=True)

    # Суммарная влажность
    total_moisture = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Плотность сухого грунта
    dry_soil_density = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    # Коэффициент теплопроводности мерзлого и талого грунта
    frozen_soil_thermal_conductivity = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    thawed_soil_thermal_conductivity = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    # Объемная теплоемкость мерзлого и талого груната
    frozen_soil_specific_heat = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    thawed_soil_specific_heat = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    # Плотность грунта
    soil_density = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    max_air_temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # температура воздуха
    max_surface_soil_temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True,
                                                   null=True)  # температура грунта на поверхности
    max_soil_temperature_5m = models.DecimalField(max_digits=5, decimal_places=2, blank=True,
                                              null=True)  # температура грунта на глубине 5 метров
    max_soil_temperature_10m = models.DecimalField(max_digits=5, decimal_places=2, blank=True,
                                               null=True)  # температура грунта на глубине 10 метров

    min_air_temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # температура воздуха
    min_surface_soil_temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True,
                                                   null=True)  # температура грунта на поверхности
    min_soil_temperature_5m = models.DecimalField(max_digits=5, decimal_places=2, blank=True,
                                              null=True)  # температура грунта на глубине 5 метров
    min_soil_temperature_10m = models.DecimalField(max_digits=5, decimal_places=2, blank=True,
                                               null=True)  # температура грунта на глубине 10 метров

    def __str__(self):
        return self.name


class Research(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    result = models.CharField(max_length=100, blank=True, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Research on {self.building.name}"


class ResearchFile(models.Model):
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    file = models.FileField(upload_to='research_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for {self.research.building.name} Research"
