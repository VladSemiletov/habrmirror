from django.urls import path

from notificationapp import views as view

app_name = 'notification'

urlpatterns = [
    path('read/', view.read, name='read'),
]