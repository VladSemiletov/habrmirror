from django.db import models
<<<<<<< HEAD
from django.utils import timezone

from authapp.models import HabUser


class HabCategory(models.Model):
    """Модель описывает категории статей"""
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Hab Categories'

    def __str__(self):
        return self.name


class Hab(models.Model):
    """Модель описывает статьи"""
    author = models.ForeignKey(HabUser, on_delete=models.CASCADE, default=0)
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=256, blank=True)
    body = models.TextField()
    category = models.ForeignKey(HabCategory, on_delete=models.CASCADE)
    creat_time = models.DateTimeField(auto_now_add=True)
    creat_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title} | {self.category}'


class Comment(models.Model):
    """Модель описывает комментарии к статьям"""
    hab = models.ForeignKey(Hab, on_delete=models.CASCADE, verbose_name='HAB', default=0)
    author = models.ForeignKey(HabUser, on_delete=models.CASCADE, default=0)
    creat_time = models.DateTimeField(auto_now_add=True)
    text = models.TextField(verbose_name="Комментарий")
    status = models.BooleanField(verbose_name="Видимость комментария", default=False)

    def __str__(self):
        return self.author
=======

# Create your models here.
>>>>>>> HAB-4
