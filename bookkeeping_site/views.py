from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import DetailView, ListView
from django.shortcuts import render, redirect

from .forms import LoginForm, RegistrationForm, AccountForm
from .models import UserAccount
from .utils import get_total_sum_account

class Page(ListView):
    """Главная страница"""
    extra_context = {
        'title': 'Главная страница',
    }
    template_name = 'bookkeeping/index.html'

    def get_queryset(self):
        pass

def login_registration(request):
    """Регистрация пользователя"""
    context = {
        'title': 'Зарегистрироваться',
        'registration_form': RegistrationForm()
    }

    return render(request, 'bookkeeping/login_registration.html', context)

def login_authentication(request):
    """Аутендификации пользователя"""
    context = {
        'title': 'Войти',
        'login_form': LoginForm()
    }

    return render(request, 'bookkeeping/login_authentication.html', context)

def user_login(request):
    """Вход в аккаунт"""
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('index')
    else:
        messages.error(request, 'Не верное имя пользователя или пароль')
        return redirect('login_authentication')

def user_logout(request):
    """Выход из аккаунта"""
    logout(request)
    return redirect('index')

def register(request):
    """Регистрация аккаунта"""
    form = RegistrationForm(data=request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Аккаунт успешно создан. Войдите в аккаунт')
    else:
        for error in form.errors:
            messages.error(request, form.errors[error].as_text())
    return redirect('login_registration')

class UserAccount(ListView):
    """Вывод счетов пользователя"""
    model = UserAccount
    context_object_name = 'accounts'
    template_name = 'bookkeeping/accounts.html'

    def get_context_data(self):
        """Получаем все счета конкретного пользователя"""
        from .models import UserAccount
        context = super().get_context_data()
        accounts = UserAccount.objects.filter(
            user=self.request.user
        )
        context['accounts'] = accounts
        context['total_sum'] = get_total_sum_account(self.request)
        return context

def account(request):
    """Страница создания счета"""
    context = {
        'title': 'Создание счета',
        'account_form': AccountForm(),
    }
    return render(request, 'bookkeeping/create_account.html', context)

def create_account(request):
    """Создание счета"""
    form = AccountForm(data=request.POST)
    if form.is_valid():
        account = form.save(commit=False)
        account.user = request.user
        account.save()
        return redirect('accounts')
    else:
        messages.error(request, 'Не верное заполнение формы!')
        return redirect('accounts')