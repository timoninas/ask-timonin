# Generated by Django 3.1.2 on 2020-11-30 20:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20201124_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birthday',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата рождения'),
        ),
    ]
