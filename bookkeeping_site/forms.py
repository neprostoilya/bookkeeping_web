from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
        
from .models import UserAccount, UserOweDebts, UserTransferToAccount, User, UserIncomes, \
    UserExpenses, User, UserDebts


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

class UserAccountForm(forms.ModelForm):
    """Форма создания счета"""
    
    class Meta:
        """Поведенческий харакатер класса"""
        model = UserAccount
        fields = ('account', 'currency', 'sum')
        widgets = {
            'account': forms.Select(attrs={
            }),
            'currency': forms.Select(attrs={
            }),
            'sum': forms.TextInput(attrs={
            })
        }

class TransferToAccountForm(forms.ModelForm):
    """Форма создания счета"""

    class Meta:
        """Поведенческий харакатер класса"""
        model = UserTransferToAccount
        fields = ('account1', 'account2', 'sum')
        widgets = {
            'account1': forms.Select(attrs={
            }),
            'account2': forms.Select(attrs={
            }),
            'sum': forms.TextInput(attrs={
            })
        }

class UserIncomeForm(forms.ModelForm):
    """Форма создания дохода"""

    class Meta:
        """Поведенческий харакатер класса"""
        model = UserIncomes
        fields = ('category', 'subcategory', 'account', 'comment', 'currency', 'sum', 'created_at')
        widgets = {
            'category': forms.Select(attrs={
            }),
            'subcategory': forms.Select(attrs={
            }),
            'account': forms.Select(attrs={
            }),
            'comment': forms.TextInput(attrs={
            }),
            'currency': forms.Select(attrs={
            }),
            'sum': forms.TextInput(attrs={
            }),
            'created_at': forms.DateInput(attrs={
                'type': 'date',
                'id': 'date_sel',
                'class': 'form-control',
            })        
        }

class UserExpenseForm(forms.ModelForm):
    """Форма создания расхода"""

    class Meta:
        """Поведенческий харакатер класса"""
        model = UserExpenses
        fields = ('category', 'subcategory', 'account', 'comment', 'currency', 'sum', 'created_at')
        widgets = {
            'category': forms.Select(attrs={
            }),
            'subcategory': forms.Select(attrs={
            }),
            'account': forms.Select(attrs={
            }),
            'comment': forms.TextInput(attrs={
            }),
            'currency': forms.Select(attrs={
            }),
            'sum': forms.TextInput(attrs={
            }),
            'created_at': forms.DateInput(attrs={
                'type': 'date',
                'id': 'date_sel',
                'class': 'form-control',
            })        
        }

class UserOweDebtForm(forms.ModelForm):
    """Форма создания долга"""

    class Meta:
        """Поведенческий харакатер класса"""
        model = UserOweDebts
        fields = ('name', 'data_1', 'data_2', 'account', 'comment', 'currency', 'sum')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            'data_1': forms.DateInput(attrs={
                'type': 'date',
                'id': 'date_sel',
                'class': 'form-control',
                'placeholder': 'Дата выдачи'
            }),
            'data_2': forms.DateInput(attrs={
                'type': 'date',
                'id': 'date_sel2',
                'class': 'form-control',
                'placeholder': 'Дата возврата'
            }),
            'comment': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Коментарий'
            }),
            'account': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Счет'
            }),
            'currency': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Валюта'
            }),
            'sum': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Сумма'
            })        
        }

class UserDebtForm(forms.ModelForm):
    """Форма создания долга"""

    class Meta:
        """Поведенческий харакатер класса"""
        model = UserDebts
        fields = ('name', 'data_1', 'data_2', 'account', 'comment', 'currency', 'sum')
        widgets = {
            'name': forms.TextInput(attrs={
            }),
            'data_1': forms.DateInput(attrs={
                'type': 'date',
                'id': 'date_sel',
                'class': 'form-control',
            }),
            'data_2': forms.DateInput(attrs={
                'type': 'date',
                'id': 'date_sel2',
                'class': 'form-control',
            }),
            'comment': forms.TextInput(attrs={
            }),
            'account': forms.Select(attrs={
            }),
            'currency': forms.Select(attrs={
            }),
            'sum': forms.TextInput(attrs={
            })        
        }

class UserReturnDebtForm(forms.ModelForm):
    """Форма возврата долга"""

    class Meta:
        """Поведенческий харакатер класса"""
        model = UserDebts
        fields = ('sum',)
        widgets = {
            'sum': forms.TextInput(),         
        }

class UserReturnOweDebtForm(forms.ModelForm):
    """Форма возврата долга"""

    class Meta:
        """Поведенческий харакатер класса"""
        model = UserOweDebts
        fields = ('sum',)
        widgets = {
            'sum': forms.TextInput(),         
        }

