from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegistrationForm(UserCreationForm):
    attrs = {'class': 'form-control'}

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs=attrs),
                               error_messages={'unique': 'Логин занят'})
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs=attrs))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs=attrs))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs=attrs),
                             error_messages={'invalid': 'Не корректно введена почта'})

    def clean(self):
        cleanedData = super().clean()
        password = cleanedData.get("password1")
        passwordRepeat = cleanedData.get("password2")
        if password != passwordRepeat:
            raise ValidationError("Пароли не совпадают")
        return cleanedData

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Почта уже используется')
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    attrs = {'class': 'form-control'}

    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs=attrs
    ))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs=attrs
    ))

    error_messages = {
        'invalid_login': 'Не верный логин или пароль'
    }

