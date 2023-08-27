from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
        
from .models import UserAccount, UserTransferToAccount, User, UserIncomes


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
    som = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Сумма'
    }))
    
    class Meta:
        """Поведенческий харакатер класса"""
        model = UserAccount
        fields = ('account', 'course', 'currency')
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

class UserIncomesForm(forms.ModelForm):
    """Форма создания дохода"""

    class Meta:
        """Поведенческий харакатер класса"""
        model = UserIncomes
        fields = ('category', 'subcategory', 'account', 'comment', 'currency', 'sum', 'created_at')
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Категория'
            }),
            'subcategory': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Зачислить на счет'
            }),
            'account': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Счет'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Коментарий'
            }),
            'currency': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Валюта'
            }),
            'sum': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Сумма'
            }),
            'created_at': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата'
            })        
        }


