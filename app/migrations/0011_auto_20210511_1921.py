# Generated by Django 3.1.4 on 2021-05-11 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20210511_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemitem',
            name='acceptance',
            field=models.DecimalField(decimal_places=2, max_digits=3),
        ),
    ]
