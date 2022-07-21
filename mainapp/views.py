from django.shortcuts import render
from core.context_service import context_update


# Create your views here.
def index(request):
    """Функция мениет контексn для главной страницы и рендерит ее"""
    context = {}
    context_update(context, key='Title', value='HabrMirror')
    return render(request, 'mainapp/index.html', context)
