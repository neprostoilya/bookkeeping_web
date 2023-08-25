from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import *


class LoginForm(AuthenticationForm):
    """Форма аутендификации"""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': "Пароль"
    }))


class RegistrationForm(UserCreationForm):
    """Форма регистрации"""
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': "Пароль"
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите пароль'
    }))

    class Meta:
        """Поведенческий харакатер класса"""
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Почта'
            })
        }

class AccountForm(forms.ModelForm):
    """Форма создания счета"""

    class Meta:
        """Поведенческий харакатер класса"""
        model = UserAccount
        fields = ('account', 'course', 'currency', 'sum')
        widgets = {
            'account': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Счет'
            }),
            'course': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Курс'
            }),
            'currency': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Валюта'
            }),
            'sum': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Сумма'
            }),
        }

class TransferToAccountForm(forms.ModelForm):
    """Форма создания счета"""
    som = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Сумма'
    }))

    class Meta:
        """Поведенческий харакатер класса"""
        model = UserTransferToAccount
        fields = ('account1', 'account2', 'course')
        widgets = {
            'account1': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Списать с счета'
            }),
            'account2': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Зачислить на счет'
            }),
            'course': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Курс перевода'
            }),

        }



