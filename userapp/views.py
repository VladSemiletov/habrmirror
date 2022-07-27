from urllib.request import Request

from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse


def logout(request: Request) -> HttpResponseRedirect:
    """Функция выхода из аккаунта"""
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

def login(request: Request) -> HttpResponseRedirect:
    """Функция авторизации"""
    pass
    return HttpResponseRedirect(reverse('index'))
