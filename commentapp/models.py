from django.db import models
from authapp.models import HabUser
from mainapp.models import Hab
from .middleware import get_current_user


class FilterComments(models.Manager):
    """
    класс - Фильтр комментариев
    """

    def get_queryset(self):
        """
        :return:
        """
        user = get_current_user()
        if not user.is_authenticated:
            return super().get_queryset().filter(comment_moderation=True)
        elif user.is_staff:
            return super().get_queryset().filter(
                models.Q(comment_moderation=True) |
                models.Q(comment_moderation=False))
        return super().get_queryset().filter(
            models.Q(comment_moderation=True,
                     comment_author=get_current_user()) |
            models.Q(comment_moderation=False,
                     comment_article__author=get_current_user()) |
            models.Q(comment_moderation=True))


class Comments(models.Model):
    """
    класс - Комментарии
    """

    class Meta:
        """
        класс - Мета
        """
        ordering = ('-pk',)
        db_table = "comments"
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    comment_author = models.ForeignKey(HabUser,
                                       verbose_name='Автор комментария',
                                       on_delete=models.CASCADE)
    comment_hab = models.ForeignKey(Hab,
                                        verbose_name='Статья',
                                        on_delete=models.CASCADE,
                                        related_name='comments_habs')
    comment_text = models.TextField('Комментарий')
    comment_create = models.DateTimeField('Дата создания', auto_now_add=True)
    comment_update = models.DateTimeField('Дата обновления', auto_now=True)
    comment_moderation = models.BooleanField('Модерация', default=True)
    is_active = models.BooleanField(verbose_name='Статус активности',
                                    default=True)
    objects = FilterComments()

    def __str__(self):
        """
        :return:
        """
        return "{}".format(self.comment_author)

    def delete(self, using=None, keep_parents=False):
        """
        Переопределение метода delete
        :param using:
        :param keep_parents:
        :return:
        """
        self.is_active = False if self.is_active else True
        self.save()
