from django.http import HttpResponseRedirect

from .models import Notification


def read(request):
    notifications = Notification.objects.filter(article_author=request.user)
    if notifications:
        for notification in notifications:
            notification.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))