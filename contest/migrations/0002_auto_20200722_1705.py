# Generated by Django 2.1.8 on 2020-07-22 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contest',
            old_name='contest_problems',
            new_name='contest_info',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='contest_length',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='contest_name',
        ),
    ]
