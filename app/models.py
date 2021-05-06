from django.db import models

CHOICES = (
    ('OIAJ', 'OIAJ'),
    ('Codeforces', 'Codeforces'),
    ('CSES', 'CSES'),
    ('SPOJ', 'SPOJ'),
    ('OnlineJudge', 'OnlineJudge')
)


class Account(models.Model):
    AccountID = models.IntegerField()
    Logik_Handle = models.CharField(max_length=30, blank=True, null=True)
    CF_Handle = models.CharField(max_length=30, blank=True, null=True)
    OIAJ_Handle = models.CharField(max_length=30, blank=True, null=True)
    CSES_Handle = models.IntegerField(blank=True, null=True)
    SPOJ_Handle = models.CharField(max_length=30, blank=True, null=True)
    OnlineJudge_Handle = models.IntegerField(blank=True, null=True)


class BlackList(models.Model):
    black_user = models.CharField(max_length=30)


class Contest(models.Model):
    contest_info = models.TextField()


class Problems(models.Model):
    judge = models.CharField(choices=CHOICES, max_length=50, default='CSES')
    problem_link = models.CharField(max_length=500)
    problem_name = models.CharField(max_length=50)
    problem_points = models.IntegerField()
    solvedBy = models.TextField()


class Recommended(models.Model):
    judge = models.CharField(choices=CHOICES, max_length=50, default='CSES')
    problem_link = models.CharField(max_length=500)
    problem_name = models.CharField(max_length=50)
    solvedBy = models.TextField()


class Tutorial(models.Model):
    id_tutorial = models.AutoField(primary_key=True)
    titulo = models.TextField()
    descripcion = models.TextField()
    autor = models.TextField()
    cuerpo = models.TextField()
    likes = models.IntegerField()
    comentarios = models.TextField()


class Contact(models.Model):
    text = models.TextField(blank=False, null=False)
