import uuid
from urllib.request import Request

from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib import auth
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import TemplateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.timezone import now

from core.context_service import context_update
from habapp.models import Hab
from authapp.forms import UserLoginForm, UserRegisterForm, UserEditForm, ProfileEditForm, HabForm, PasswordChangeForm
from authapp.models import HabUser, HabProfile
from notificationapp.models import NotifyUser
from ratingapp.models import AuthorRating


class SendVerifyMail:
    """ Отправка сообщения пользователю """

    def __init__(self, user):

        verify_link = reverse('auth:verify', args=[
            user.email, user.activation_key])  # Генерация ссылки

        subject = f'подтверждение учётной записи {user.username}'

        message = f'Для подтверждения учетной записи {user.username} на портале \
            {settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


class VerifyView(TemplateView):
    """ Проверка ключа активации """

    def get(self, request, email, activation_key):
        try:
            user = HabUser.objects.get(email=email)
            if user.activation_key == activation_key and not user.is_activation_key_expired():
                user.is_active = True
                user.activation_key = None
                user.activation_key_expires = now()
                user.save()
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return HttpResponseRedirect(reverse('main'))
            else:
                print(f'ошибка активации пользователя: {user}')
                return render(request, 'authapp/verification.html')
        except Exception as ex:
            return HttpResponseRedirect(reverse('main'))


# @csrf_exempt
class LoginUserView(LoginView):
    """ Контроллер входа в системы """
    template_name = 'authapp/login.html'
    form_class = UserLoginForm


class LogoutUserView(LogoutView):
    """ Контроллер выхода из системы """

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class RegisterUserView(SuccessMessageMixin, CreateView):
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('auth:login')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"

    def post(self, request, *args, **kwargs):
        """ Проверяем форму регистрации """

        register_form = UserRegisterForm(request.POST, request.FILES)

        if request.method == "POST":
            if register_form.is_valid():
                if HabUser.objects.all().filter(email=register_form.data['email']):
                    context = {
                        'error': f'пользователь уже зарегистрирован с данным EMAIL:{register_form.data["email"]}'}
                    return render(request, 'authapp/error.html', context)
                user = register_form.save()
                # SendVerifyMail(user)
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                context = {'error': f'Форма заполнена не корректна'}
                return render(request, 'authapp/error.html', context)
        else:
            return render(
                request,
                HttpResponseRedirect(reverse('main')),
                {}
            )


def messages(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('messages'))

    return render(request, 'authapp/messages.html')


class UserIsUserMixin(UserPassesTestMixin):
    """ Предоставляет право доступа пользователю у которого роль Администратор """

    def test_func(self):
        return True


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """ Редактирование профиля """
    model = HabUser
    template_name = 'authapp/edit.html'
    form_class = UserEditForm
    second_form_class = ProfileEditForm

    def get_success_url(self):
        pk = self.object.pk
        return reverse('auth:profile', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(ProfileEditView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(instance=self.object)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=HabProfile.objects.get(id=self.kwargs['pk']))
        context['avatar'] = self.object.avatar
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form2 = self.second_form_class(request.POST, instance=HabProfile.objects.get(id=self.kwargs['pk']))
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid() and form2.is_valid():
            form2.save()
            return super().post(request, *args, **kwargs)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, form2=form2))


class UserDetailView(DetailView):
    """ Страница профиля """
    model = HabUser
    template_name = 'authapp/user_detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        habs = Hab.objects.all().filter(author=self.object)
        context['habs_draft'] = habs.filter(status='DF')
        context['habs_moder'] = habs.filter(status='PB', approve=False)
        context['habs_public'] = habs.filter(status='PB', approve=True)

        try:
            rating = get_object_or_404(AuthorRating, author=self.object)
            context['rating'] = rating.value()

        except Exception:
            # TODO обработать конкретное исключение
            pass
        context['notify'] = NotifyUser.objects.all().filter(user_to=self.object)

        return context


class UserChangePassword(LoginRequiredMixin, PasswordChangeView):
    """ Сменя пароля """
    template_name = 'authapp/change_pass.html'
    form_class = PasswordChangeForm

    def get_success_url(self):
        return reverse('auth:profile', kwargs={'pk': self.request.user.pk})


def notification_view(request: Request, user_id: int) -> HttpResponse:
    """Конроллер для страницы уведомлений пользователя"""
    context ={}
    notification_to_user = NotifyUser.objects.select_related('hab').filter(user_to=user_id)
    context_update(context, 'notify', notification_to_user )

    return render(request, 'authapp/account/notification.html', context)