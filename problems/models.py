from django.db import models

# Create your models here.
class Problems(models.Model):
    oiaj=models.BooleanField()
    problem_link=models.CharField(max_length=100)
    problem_name=models.CharField(max_length=50)
    problem_points=models.IntegerField()
    solvedBy=models.TextField()