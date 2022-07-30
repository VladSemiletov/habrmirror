from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse

from authapp.forms import HabUserLoginForm, HabUserRegisterForm, HabUserAccountForm


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
    return render(request, 'authapp/login.html', context)


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

    context = {
        'register_form': register_form
    }
    return render(request, 'authapp/register.html', context)


def account(request):
    if request.method == 'POST':
        account_form = HabUserAccountForm(request.POST, request.FILES, instance=request.user)
        if account_form.is_valid():
            account_form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        account_form = HabUserAccountForm(instance=request.user)

    context = {
        'account_form': account_form
    }
    return render(request, 'authapp/account.html', context)