from django.shortcuts import render


# Create your views here.
def index(request):
    """Функция мениет контексn для главной страницы и рендерит ее"""
    context = {}
    return render(request, 'mainapp/index.html', context)
