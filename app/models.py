from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.db import models

class ProfileManager(models.Manager):
    def best(self):
        return self.order_by('-rating')[:5]

class Profile(models.Model):
    #null=True
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, verbose_name='Имя')
    birthday = models.DateField(verbose_name='Дата рождения')
    image = models.ImageField(default='default.png', blank=True)
    rating = models.PositiveIntegerField(default=0, verbose_name="Рейтинг")

    objects = ProfileManager()

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class QuestionManager(models.Manager):
    def newest(self):
        return self.filter(active_status=True).order_by('-data_create')

    def hottest(self):
        return self.filter(active_status=True).order_by('-views')

    def tagged(self, title):
        return self.filter(active_status=True, tags__title=title)

class Question(models.Model):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.CharField(max_length=1024, verbose_name='Текст')
    data_create = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    views = models.PositiveIntegerField(default=1, db_index=True, verbose_name="Количество просмотров")
    active_status = models.BooleanField(default=True, verbose_name="Статус активности")
    answers_number = models.PositiveIntegerField(default=0, verbose_name="Количество ответов")

    author = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name="Автор вопроса")
    likes = models.ManyToManyField('Profile', related_name='comments', default=None, blank=True, verbose_name="Лайки пользователей")
    tags = models.ManyToManyField('Tag', blank=True, verbose_name="Теги")

    objects = QuestionManager()

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class CommentManager(models.Manager):
    def newest(self, id):
        q = Question.objects.get(pk=id)
        return self.filter(question=q).order_by('-data_create')

class Comment(models.Model):
    text = models.CharField(max_length=1024, verbose_name='Текст')
    views = models.PositiveIntegerField(default=1, db_index=True, verbose_name="Количество просмотров")
    data_create = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    correct_status = models.BooleanField(default=False, verbose_name="Корректность ответа")

    author = models.ForeignKey('Profile', on_delete=models.PROTECT)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name="Вопрос")

    objects = CommentManager()

    def __str__(self):
        return '{} : "{}"'.format(self.author.name, self.text)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class TagManager(models.Manager):
    def popular(self):
        return self.order_by('-references')[:7]

class Tag(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название тега')
    references = models.PositiveIntegerField(default=0)

    objects = TagManager()

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'