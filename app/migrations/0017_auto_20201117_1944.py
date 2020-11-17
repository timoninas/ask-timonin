# Generated by Django 3.1.2 on 2020-11-17 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20201117_1929'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='likes',
        ),
        migrations.AddField(
            model_name='comment',
            name='correct_status',
            field=models.BooleanField(default=False, verbose_name='Корректность ответа'),
        ),
        migrations.AddField(
            model_name='comment',
            name='views',
            field=models.PositiveIntegerField(db_index=True, default=1, verbose_name='Количество просмотров'),
        ),
        migrations.AlterField(
            model_name='question',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile', verbose_name='Автор вопроса'),
        ),
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(blank=True, to='app.Tag', verbose_name='Теги'),
        ),
    ]
