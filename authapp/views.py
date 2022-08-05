from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse



from habapp.models import Hab
from authapp.forms import UserLoginForm, UserRegisterForm, UserEditForm, ProfileEditForm, HabForm, PasswordChangeForm
from authapp.models import HabUser
from notificationapp.models import NotifyUser
from ratingapp.models import AuthorRating


class SendVerifyMail:
    """ Отправка сообщения пользователю """


def login(request):
    login_form = HabUserLoginForm(data=request.POST or None)
    next_param = request.GET.get('next', '')

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            return HttpResponseRedirect(reverse('index'))

    context = {
        'login_form': login_form,
        'next': next_param
    }
    return render(request, 'authapp/auth/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        register_form = HabUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        register_form = HabUserRegisterForm()



# @csrf_exempt
class LoginUserView(LoginView):
    """ Контроллер входа в системы """
    template_name = 'authapp/auth/login.html'
    form_class = UserLoginForm



def account(request):
    if request.method == 'POST':
        account_form = HabUserAccountForm(request.POST, request.FILES, instance=request.user)
        if account_form.is_valid():
            account_form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        account_form = HabUserAccountForm(instance=request.user)


    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class RegisterUserView(SuccessMessageMixin, CreateView):
    template_name = 'authapp/auth/register.html'
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
                    return render(request, 'authapp/auth/error.html', context)
                user = register_form.save()
                SendVerifyMail(user)
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                context = {'error': f'Форма заполнена не корректна'}
                return render(request, 'authapp/auth/error.html', context)
        else:
            return render(
                request,
                HttpResponseRedirect(reverse('main')),
                {}
            )


def messages(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('messages'))

    return render(request, 'authapp/account/messages.html')


def habs_test(request):
    if request.method == 'POST':
        hab_form = HabForm(request.POST)
        if hab_form.is_valid():
            return HttpResponseRedirect(reverse('habs_test'))
    else:
        hab_form = HabForm()

    context = {
        'hab_form': hab_form
    }
    return render(request, 'authapp/account/habs.html', context)


class UserIsUserMixin(UserPassesTestMixin):
    """ Предоставляет право доступа пользователю у которого роль Администратор """

    def test_func(self):
        return True


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """ Редактирование профиля """
    model = HabUser
    template_name = 'authapp/auth/edit.html'
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
            context['form2'] = self.second_form_class(instance=self.object.habrprofile)
        context['avatar'] = self.object.avatar
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form2 = self.second_form_class(request.POST, instance=self.object.habrprofile)
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
    template_name = 'authapp/account/account.html'
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
    template_name = 'auth/change_pass.html'
    form_class = PasswordChangeForm

    def get_success_url(self):
        return reverse('auth:profile', kwargs={'pk': self.request.user.pk})

