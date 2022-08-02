from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from authapp.models import HabUser
from mainapp.models import Hab


class HabUserLoginForm(AuthenticationForm):
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


class HabUserAccountForm(UserChangeForm):
    class Meta:
        model = HabUser
        fields = ('username', 'first_name', 'email', 'age', 'avatar', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

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


class HabForm(forms.ModelForm):

    class Meta:
        model = Hab
        exclude = ('author', 'description', 'category',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
