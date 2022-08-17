from django.urls import path

from authapp import views as authapp
from authapp.views import LoginUserView, LogoutUserView, RegisterUserView, VerifyView, ProfileEditView, UserDetailView, \
    UserChangePassword, notification_view
from django.urls import include, re_path

app_name = 'authapp'

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    # path('account/', authapp.account, name='account'),
    path('save_form/', authapp.save_form, name='save_form'),
    path('messages/', authapp.messages, name='messages'),

    path('delete_hab/<uuid:pk>/', authapp.delete_hab, name='delete_hab'),


    # path('edit/<int:pk>/', ProfileEditView.as_view(), name='edit'),
    path('create_hab/', authapp.create_hab, name='create_hab'),
    path('habs/', authapp.hab_set, name='habs'),
    path('verify/<email>/<activation_key>', VerifyView.as_view(), name='verify'),
    path('profile/<int:pk>', ProfileEditView.as_view(), name='profile'),
    path('change-password/', UserChangePassword.as_view(), name='change_pass'),
    path('notification/<int:user_id>/', authapp.notification_view, name='user_notificftion'),
]


