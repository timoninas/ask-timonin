# Generated by Django 3.1.2 on 2020-11-17 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20201117_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(blank=True, default=None, related_name='posts', to='app.Profile', verbose_name='Лайки пользователей'),
        ),
    ]
