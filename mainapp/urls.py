from django.urls import path, include

from mainapp.views import main

app_name = 'mainapp'

urlpatterns = [
    path('', main, name='index'),
]