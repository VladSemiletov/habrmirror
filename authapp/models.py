from django.db import models
from django.contrib.auth.models import AbstractUser


class HabUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True, verbose_name='картинка')
    age = models.PositiveIntegerField(verbose_name='возраст')


class UserProfile(models.Model):
    """Модель профиля пользователя"""
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(HabUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    about_me = models.TextField(verbose_name='О себе', max_length=512, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, max_length=1, verbose_name='пол')
