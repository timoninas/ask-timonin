# Generated by Django 3.1.2 on 2020-11-24 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('app', '0019_auto_20201124_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.PositiveIntegerField(db_index=True, default=0, verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='question',
            name='rating',
            field=models.PositiveIntegerField(db_index=True, default=0, verbose_name='Рейтинг'),
        ),
        migrations.CreateModel(
            name='LikeDislike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(default=0, verbose_name='Like or not')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voted', to='app.profile')),
            ],
            options={
                'verbose_name': 'Лайк или дизлайк',
                'verbose_name_plural': 'Лайки или дизлайки',
            },
        ),
    ]
