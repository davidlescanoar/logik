from django.db import models

CHOICES = (
   ('OIAJ', 'OIAJ'),
   ('Codeforces', 'Codeforces'),
   ('CSES', 'CSES'),
   ('SPOJ', 'SPOJ'),
   ('OnlineJudge', 'OnlineJudge')
)

# Create your models here.
class Problems(models.Model):
    judge=models.CharField(choices=CHOICES, max_length=50, default='CSES')
    problem_link=models.CharField(max_length=500)
    problem_name=models.CharField(max_length=50)
    problem_points=models.IntegerField()
    solvedBy=models.TextField()