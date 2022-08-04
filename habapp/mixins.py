from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404

from habapp.models import Hab


class UserIsNoBlockMixin(UserPassesTestMixin):
    """ Предоставляет право доступа пользователю который не заблокирован """

    def test_func(self):
        user = self.request.user
        author = get_object_or_404(Hab, pk=self.kwargs['pk']).author
        if user.is_authenticated:
            if user == author:
                return user.check_block() is False

    def handle_no_permission(self):
        return redirect('/')
