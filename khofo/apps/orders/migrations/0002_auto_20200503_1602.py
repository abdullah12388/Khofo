# Generated by Django 2.2.9 on 2020-05-03 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
        ('products', '0001_initial'),
        ('delegates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Category', verbose_name='category'),
        ),
        migrations.AddField(
            model_name='order',
            name='delegate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='delegates.Delegate', verbose_name='delegate'),
        ),
    ]