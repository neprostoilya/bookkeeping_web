from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
        
from .models import CategoriesAccounts, CategoriesCurrencys, CategoriesCurrencys, CategoriesExpenses, CategoriesIncomes, \
    UserAccounts, UserOweDebts, UserTransferToAccount, User, UserIncomes, UserExpenses, User, UserDebts



class LoginForm(forms.Form):
    """Форма аутендификации"""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': "Пароль"
    }))

    def __init__(self, *args, **kwargs):
        """Кастомные заголовки"""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].label = 'Пароль'
        self.fields['username'].label = 'Имя пользователя'

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

    def __init__(self, *args, **kwargs):
        """Кастомные заголовки"""
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтвердите пароль'

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
        model = UserAccounts
        fields = ('account', 'currency', 'sum')
        widgets = {
            'account': forms.Select(attrs={
            }),
            'currency': forms.Select(attrs={
            }),
            'sum': forms.TextInput(attrs={
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = CategoriesAccounts.objects.filter(user=user)
        self.fields['currency'].queryset = CategoriesCurrencys.objects.filter(user=user)

class UserTransferToAccountForm(forms.ModelForm):
    """Форма создания счета"""

    class Meta:
        """Поведенческий харакатер класса"""
        model = UserTransferToAccount
        fields = ('account1', 'account2', 'currency', 'sum')
        widgets = {
            'account1': forms.Select(attrs={
            }),
            'account2': forms.Select(attrs={
            }),
            'currency': forms.Select(attrs={
            }),
            'sum': forms.TextInput(attrs={
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['account1'].queryset = UserAccounts.objects.filter(user=user)
        self.fields['account2'].queryset = UserAccounts.objects.filter(user=user)
        self.fields['currency'].queryset = CategoriesCurrencys.objects.filter(user=user)

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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = CategoriesIncomes.objects.filter(user=user)
        self.fields['subcategory'].queryset = CategoriesIncomes.objects.filter(user=user)
        self.fields['account'].queryset = UserAccounts.objects.filter(user=user)
        self.fields['currency'].queryset = CategoriesCurrencys.objects.filter(user=user)

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
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = CategoriesExpenses.objects.filter(user=user)
        self.fields['subcategory'].queryset = CategoriesExpenses.objects.filter(user=user)
        self.fields['account'].queryset = UserAccounts.objects.filter(user=user)
        self.fields['currency'].queryset = CategoriesCurrencys.objects.filter(user=user)

class UserOweDebtForm(forms.ModelForm):
    """Форма создания долга"""

    class Meta:
        """Поведенческий харакатер класса"""
        model = UserOweDebts
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = UserAccounts.objects.filter(user=user)
        self.fields['currency'].queryset = CategoriesCurrencys.objects.filter(user=user)

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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = UserAccounts.objects.filter(user=user)
        self.fields['currency'].queryset = CategoriesCurrencys.objects.filter(user=user)

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

class CategoryAccountForm(forms.ModelForm):
    """Форма создания категории счета"""

    class Meta:
        """Поведенческий харакатер класса"""
        model = CategoriesAccounts
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(),         
        }

class CategoryIncomeForm(forms.ModelForm):
    """Форма создания категории дохода"""

    class Meta:
        """Поведенческий харакатер класса"""
        model = CategoriesIncomes
        fields = ('title', 'subcategory')
        widgets = {
            'title': forms.TextInput(), 
            'subcategory': forms.Select()  
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = CategoriesIncomes.objects.filter(user=user)

class CategoryExpenseForm(forms.ModelForm):
    """Форма создания категории расхода"""

    class Meta:
        """Поведенческий харакатер класса"""
        model = CategoriesExpenses
        fields = ('title', 'subcategory')
        widgets = {
            'title': forms.TextInput(),      
            'subcategory': forms.Select()  
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = CategoriesExpenses.objects.filter(user=user)

class CategoryCurrencyForm(forms.ModelForm):
    """Форма создания категории валюты"""

    class Meta:
        """Поведенческий харакатер класса"""
        model = CategoriesCurrencys
        fields = ('title', 'course')
        widgets = {
            'title': forms.TextInput(),   
            'course': forms.TextInput(),      
        }