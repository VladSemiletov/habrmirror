from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms



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
        super().__init__(*args, **kwargs)
        print(self.fields.items())
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # field.widget.attrs['placeholder'] = field_name
            field.help_text = ''


class HabUserRegisterForm(UserCreationForm):
    class Meta:
        model = HabUser
        fields = ('username', 'first_name', 'last_name', 'email', 'age', 'avatar', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def save(self):
    # def save(self, *args, **kwargs):
        user = super().save()


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


class HabUserAccountForm(UserChangeForm):
    class Meta:
        model = HabUser
        fields = ('username', 'first_name', 'email', 'age', 'avatar', 'password')

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
        exclude = ('author', 'description', 'category',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

