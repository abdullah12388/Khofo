# Generated by Django 2.2.9 on 2020-05-03 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0002_adsmanager_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='show_num',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='show_num'),
        ),
    ]
