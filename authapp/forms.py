from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import fields
from .models import HabUser, HabProfile
from django.contrib.auth import forms as auth_forms


from authapp.models import HabUser
from habapp.models import Hab

from django.contrib.auth.forms import UserChangeForm


import random
import hashlib

CHECK_LIST = ['is_active', 'is_delete', 'is_staff', 'is_deleted']


def add_class_html(fields):
    for field_name, field in fields.items():
        if field_name in CHECK_LIST:
            field.widget.attrs['class'] = 'form-chek'
            field.help_text = ''
            continue
        else:
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = HabUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = HabUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1',
                  'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def save(self):
    # def save(self, *args, **kwargs):
        user = super().save()

        user.is_active = True
        # salt = hashlib.sha1(
        #     str(random.random()).encode('utf8')).hexdigest()[:6]
        #
        # user.activation_key = hashlib.sha1(
        #     (user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user


class UserEditForm(forms.ModelForm):
    """ Форма редактирование пользователя """
    class Meta:
        model = HabUser
        fields = ('username', 'first_name', 'last_name', 'email', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_class_html(self.fields)

    def clean_age(self):
        data = self.cleaned_data['age']
        if data > 100:
            raise forms.ValidationError('Со всем почтением Ваш возраст слишком велик.')
        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        if len(data) > 24:
            raise forms.ValidationError('Слишком длинный ник.')
        return data

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if len(data) > 24:
            raise forms.ValidationError('Слишком длинное имя.')
        return data

    def clean_avatar(self):
        data = self.cleaned_data['avatar']
        print(bool(data))
        if data:
            return data
        data = "{% static 'img/user_photo.png' %}"
        return data


class ProfileEditForm(forms.ModelForm):
    """ Форма редактирование профиля """

    class Meta:
        model = HabProfile
        fields = ('tagline', 'gender', 'birthday', 'zone')

    birthday = forms.DateField(label='Дата рождения',
                               required=True,
                               widget=forms.SelectDateWidget(years=range(1950, 2010)),
                               )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_class_html(self.fields)


class PasswordChangeForm(auth_forms.PasswordChangeForm):
    class Meta:
        model = HabUser
        fields = ('old_password', 'new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        add_class_html(self.fields)


class HabForm(forms.ModelForm):

    class Meta:
        model = Hab
        exclude = 'category', 'created', 'updated', 'status', 'liked', 'approve', 'publication_date'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
