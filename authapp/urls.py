from django.urls import path
from authapp import views as authapp


app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/', authapp.register, name='register'),
    path('account/', authapp.account, name='account'),
]
