from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
class Profile(models.Model):
    #null=True
    name = models.CharField(max_length=256, verbose_name='Имя')
    birthday = models.DateField(verbose_name='Дата рождения')
    image = models.ImageField(default='default.png', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class Question(models.Model):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.CharField(max_length=1024, verbose_name='Текст')
    data_create = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Comment(models.Model):
    text = models.CharField(max_length=1024, verbose_name='Текст')
    data_create = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name="Вопрос")

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class Tag(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название тега')
    tags = models.ManyToManyField('Question', verbose_name="Вопрос")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'