from django.db import models
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
