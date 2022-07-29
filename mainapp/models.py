from datetime import datetime
from datetime import date

from django.db import models

# Create your models here.
from django.utils import timezone

from authapp.models import HabUser
# from userapp.models import User


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
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=256, blank=True)
    body = models.TextField()
    category = models.ForeignKey(HabCategory, on_delete=models.CASCADE)
    creat_time = models.DateTimeField(auto_now_add=True)
    creat_time = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(HabUser, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return f'{self.title} | {self.category}'
