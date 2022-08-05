from django.db import models

from habapp.models import Hab
from authapp.models import HabUser


class HabRating(models.Model):
    """ Рейтинг статьи """

    class Meta:
        verbose_name = "рейтинг статьи"
        verbose_name_plural = "рейтинги статей"

    hab = models.OneToOneField(Hab, verbose_name='статья', primary_key=True, on_delete=models.DO_NOTHING)
    likes = models.PositiveIntegerField(verbose_name='количество лайков', default=0)
    comments = models.PositiveIntegerField(verbose_name='количество комментариев', default=0)

    def value(self):
        """ рейтинг """
        return self.likes + self.comments

    @property
    def rating(self):
        return self.value()


class AuthorRating(models.Model):
    """ Рейтинг автора """

    class Meta:
        verbose_name = "рейтинг пользователя"
        verbose_name_plural = "рейтинги пользователей"

    author = models.OneToOneField(HabUser, verbose_name='статья', primary_key=True, on_delete=models.DO_NOTHING)
    likes = models.PositiveIntegerField(verbose_name='количество лайков', default=0)
    comments = models.PositiveIntegerField(verbose_name='количество комментариев', default=0)

    def value(self):
        """ рейтинг """
        return self.likes + self.comments

