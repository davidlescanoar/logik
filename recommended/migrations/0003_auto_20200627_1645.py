# Generated by Django 2.1.8 on 2020-06-27 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommended', '0002_auto_20200627_1644'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recommended',
            old_name='oiaj',
            new_name='judge',
        ),
    ]
