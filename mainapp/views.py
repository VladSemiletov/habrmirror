from django.shortcuts import render
from core.context_service import context_update

# Create your views here.
from mainapp.service_mainapp import last_hub


def index(request):
    """Функция обновляет контекст для главной страницы и рендерит ее"""
    context = {}
    context_update(context, key='Title', value='HabrMirror')
    context_update(context, key='hab', value=last_hub())
    return render(request, 'mainapp/index.html', context)
