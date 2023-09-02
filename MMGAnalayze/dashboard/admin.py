from django.contrib import admin
from .models import *

# Register your models here.

class CompanyAdmin(admin.ModelAdmin):
    #Вывод в читаемом виде
    list_display = [field.name for field in CompanySensor._meta.fields]
    #Редактируемые поля
    list_editable = ("name","description")
    # Список полей, по которым будет поиск в таблице
    search_fields = ['name']
    # Список полей, по которым будут фильтроваться записи в админке (панель)
    list_filter = ['name']

    class Meta:
        model = CompanySensor

class SensorAdmin(admin.ModelAdmin):
    #Вывод в читаемом виде
    list_display = [field.name for field in Sensor._meta.fields]
    #Редактируемые поля
    list_editable = ['model', "description", "manufacturer"]
    # Список полей, по которым будет поиск в таблице
    search_fields = ['model']
    # Список полей, по которым будут фильтроваться записи в админке (панель)
    list_filter = ['model']

    class Meta:
        model = Sensor


class SensorReadingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SensorReading._meta.fields]
    search_fields = ['sensor__model']
    list_filter = ['sensor__model']

    class Meta:
        model = SensorReading

# Register your models here.
admin.site.register(CompanySensor, CompanyAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(SensorReading, SensorReadingAdmin)