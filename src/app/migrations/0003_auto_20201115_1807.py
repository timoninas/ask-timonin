# Generated by Django 3.1.2 on 2020-11-15 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20201115_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tags',
            field=models.ManyToManyField(to='app.Question', verbose_name='Вопрос'),
        ),
    ]
