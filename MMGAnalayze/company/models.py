from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    name = models.CharField(blank=False, null=False, unique=True,
                            max_length=128)
    def __str__(self):
        return self.name

class UserCompany(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, unique=True,
                             on_delete=models.CASCADE)
    company = models.ForeignKey(Company, blank=False, null=False,
                                on_delete=models.CASCADE)


class UserRight(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, unique=True,
                             on_delete=models.CASCADE)
    can_control_user_company = models.BooleanField(null=False, blank=False,
                                                   default=False)
    can_control_monitoring_object = models.BooleanField(null=False, blank=False,
                                                        default=False)
