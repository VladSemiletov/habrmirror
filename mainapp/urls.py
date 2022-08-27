from django.urls import path, include

from mainapp.views import main, help

app_name = 'mainapp'

urlpatterns = [
    path('', main, name='index'),
    path('help', help, name='help'),
]
