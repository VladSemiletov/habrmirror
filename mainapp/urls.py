from django.urls import path, include

from mainapp.views import main, help

app_name = 'mainapp'

urlpatterns = [
    path('', main, name='main'),
    path('index/', main),
]
