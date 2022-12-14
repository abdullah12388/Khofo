# Generated by Django 2.2.9 on 2020-05-03 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=500, verbose_name='address')),
                ('working_field', models.CharField(max_length=500, verbose_name='working_field')),
                ('phone', models.CharField(max_length=100, verbose_name='phone')),
                ('website', models.URLField(max_length=1000, verbose_name='website')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created_on')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='modified_on')),
            ],
            options={
                'verbose_name': 'Provider',
                'verbose_name_plural': 'Providers',
            },
        ),
    ]
