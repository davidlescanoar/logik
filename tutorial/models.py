from django.db import models

# Create your models here.
class Tutorial(models.Model):
    id_tutorial = models.AutoField(primary_key=True)
    titulo=models.TextField()
    descripcion=models.TextField()
    autor=models.TextField()
    cuerpo=models.TextField()
    likes=models.IntegerField()
    comentarios=models.TextField()