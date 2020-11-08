from django.db import models

# Create your models here.
class Author(models.Model):
    #null=True
    name = models.CharField(max_length=256, verbose_name='Имя')
    birthday = models.DateField(verbose_name='Дата рождения')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Имя')
    #text  =
    #data_create =

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'