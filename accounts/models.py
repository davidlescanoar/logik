from django.db import models

# Create your models here.

class Account(models.Model):
    AccountID=models.IntegerField()
    Logik_Handle=models.CharField(max_length=30, blank=True, null=True)
    CF_Handle=models.CharField(max_length=30, blank=True, null=True)
    OIAJ_Handle=models.CharField(max_length=30, blank=True, null=True)