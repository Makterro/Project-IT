from django.contrib import admin
from .models import Company, UserCompany, UserRight

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class UserCompanyAdmin(admin.ModelAdmin):
    list_display = ['user', 'company']
    search_fields = ['user__username', 'company__name']

class UserRightAdmin(admin.ModelAdmin):
    list_display = ['user', 'can_control_user_company', 'can_control_monitoring_object']
    search_fields = ['user__username']

admin.site.register(Company, CompanyAdmin)
admin.site.register(UserCompany, UserCompanyAdmin)
admin.site.register(UserRight, UserRightAdmin)