from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from habapp.models import Hab
from authapp.models import HabUser
from commentapp.models import Comments


class NotifyUser(models.Model):
    """ Модель уведомления пользователя """

    class Meta:
        ordering = ('-created',)
        verbose_name = 'уведомление пользователя'
        verbose_name_plural = 'уведомления пользователей'

    LIKE = 'L'
    REMOVE_LIKE = 'R'
    COMMENT = 'C'
    APPROVE = 'A'
    BLOCK = 'B'
    UNBLOCK = 'U'

    TYPE_NOTIFY = {
        (LIKE, 'поставлен лайк'),
        (REMOVE_LIKE, 'убран лайк'),
        (COMMENT, 'комментарий'),
        (APPROVE, 'подтверждение статьи'),
        (BLOCK, 'блокировка пользователя'),
        (UNBLOCK, 'разблокировка пользователя'),
    }

    user_to = models.ForeignKey(HabUser, on_delete=models.CASCADE)
    from_user = models.ForeignKey(HabUser, on_delete=models.CASCADE, related_name='from_user', blank=True, null=True)
    type_notify = models.CharField('Тип уведомления', choices=TYPE_NOTIFY, max_length=1)
    hab = models.ForeignKey(Hab, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField('Дата создания', auto_now_add=now)
    is_read = models.BooleanField('Статус прочтения', default=False)

    def delete(self, using=None, keep_parents=False):
        """ Переопределение удаления комментария """

        self.is_read = True
        self.save()

    @receiver(post_save, sender=Comments)
    def add_comment_notify(sender, instance, created, **kwargs):
        """ Создание уведомления при новом комментарии статьи """

        if created:
            notify = NotifyUser()
            notify.user_to = HabUser.objects.get(pk=instance.comment_hab.author.pk)
            notify.from_user = HabUser.objects.get(pk=instance.comment_author.pk)
            notify.type_notify = notify.COMMENT
            notify.hab = Hab.objects.get(uid=instance.comment_hab.uid)
            notify.save()

    @receiver(post_save, sender=Hab)
    def approve_hab_notify(sender,  instance, **kwargs):
        """ Создание уведомления при положительной модерации статьи """

        if kwargs['update_fields']:
            notify = NotifyUser()
            notify.user_to = HabUser.objects.get(pk=instance.author.pk)
            notify.type_notify = notify.APPROVE
            notify.hab = Hab.objects.get(uid=instance.uid)
            notify.save()

    # @receiver(post_save, sender=HabUser)
    # def block_user_notify(sender, instance, **kwargs):
    #     """ Создание уведомления при блокировке/разблокировке пользователя """
    #
    #     today = now()
    #     block = instance.is_block
    #     check_date = timedelta(seconds=1)
    #     timedelta_date = block - today
    #
    #     if kwargs['update_fields'] == {'is_block'}:
    #         notify = NotifyUser()
    #         notify.user_to = HabUser.objects.get(pk=instance.pk)
    #         if timedelta_date > check_date:
    #             notify.type_notify = notify.BLOCK
    #         else:
    #             notify.type_notify = notify.UNBLOCK
    #         notify.save()
    #
    # @receiver(m2m_changed, sender=Hab.liked.through)
    def add_like_notify(sender, instance, **kwargs):
        """ Создание уведомления при новом лайке/ удалении лайка  """

        notify = NotifyUser()
        from_user, *_ = kwargs['pk_set']

        notify.user_to = HabUser.objects.get(pk=instance.author.pk)
        notify.from_user = HabUser.objects.get(pk=from_user)
        notify.hab = Hab.objects.get(uid=instance.uid)

        if kwargs['action'] == 'post_add':
            notify.type_notify = notify.LIKE
            notify.save()
        elif kwargs['action'] == 'post_remove':
            notify.type_notify = notify.REMOVE_LIKE
            notify.save()
