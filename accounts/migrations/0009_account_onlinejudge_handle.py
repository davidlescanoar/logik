# Generated by Django 2.1.8 on 2020-08-14 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20200801_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='OnlineJudge_Handle',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
