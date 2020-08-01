from django.db import models

CHOICES = (
   ('OIAJ', 'OIAJ'),
   ('Codeforces', 'Codeforces'),
   ('CSES', 'CSES'),
   ('SPOJ', 'SPOJ')
)

# Create your models here.
class recommended(models.Model):
    judge=models.CharField(choices=CHOICES, max_length=50, default='CSES')
    problem_link=models.CharField(max_length=100)
    problem_name=models.CharField(max_length=50)
    solvedBy=models.TextField()