from django.db import models

# Create your models here.
class recommended(models.Model):
    oiaj=models.BooleanField()
    problem_link=models.CharField(max_length=100)
    problem_name=models.CharField(max_length=50)
    solvedBy=models.TextField()