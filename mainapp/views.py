from urllib.request import Request

from django.http import HttpResponse
from django.shortcuts import render
from core.context_service import context_update

# Create your views here.
from mainapp.service_mainapp import last_hub, all_HabCategory


def index(request: Request) -> HttpResponse:
    """Функция мениет контекст для главной страницы и рендерит ее"""
    context = {}
    context_update(context, key='Title', value='HabrMirror')
    context_update(context, key='hab', value=last_hub(5))
    context_update(context, key='hab_category', value=all_HabCategory())
    return render(request, 'mainapp/index.html', context)

def category(request: Request, pk: int) -> HttpResponse:
    pass

