from django.db import models

# Create your models here.

class BlackList(models.Model):
    black_user=models.CharField(max_length=30)