from django.contrib import admin
from .models import *

# Register your models here.

class BuildingAdmin(admin.ModelAdmin):
    # Вывод в читаемом виде
    list_display = [field.name for field in Building._meta.fields]
    # Редактируемые поля
    list_editable = ("name", "telephone", "description")
    # Список полей, по которым будет поиск в таблице
    search_fields = ['name']
    # Список полей, по которым будут фильтроваться записи в админке (панель)
    list_filter = ['name']

    class Meta:
        model = Building

class ResearchAdmin(admin.ModelAdmin):
    class Meta:
        model = Research

class ResearchFileAdmin(admin.ModelAdmin):
    class Meta:
        model = ResearchFile

admin.site.register(Building, BuildingAdmin)
admin.site.register(Research, ResearchAdmin)
admin.site.register(ResearchFile, ResearchFileAdmin)
