import datetime
from typing import Any

from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models.query import QuerySet
from django.views.generic import ListView
from django.shortcuts import render, redirect

from .forms import LoginForm, RegistrationForm, AccountForm, TransferToAccountForm,  \
        UserIncomesForm, UserExpensesForm
from .models import UserAccount, UserIncomes, UserExpenses
from .utils import get_total_sum_account, save_transfer_sum, save_income_sum, save_expenses_sum, \
        get_total_sum_incomes, get_total_sum_expenses

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

class UserAccountPage(ListView):
    """Страничка счетов пользователя"""
    extra_context = {
        'title': 'Счета',
    }
    model = UserAccount
    context_object_name = 'accounts'
    template_name = 'bookkeeping/accounts.html'

    def get_context_data(self):
        context = super().get_context_data()
        accounts = UserAccount.objects.filter(
            user=self.request.user
        )
        context['accounts'] = accounts
        context['total_sum'] = get_total_sum_account(self.request)
        return context

def create_account_page(request):
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
        account.sum = int(form.cleaned_data['som']) * account.course
        account.save()
        return redirect('accounts')
    else:
        messages.error(request, 'Не верное заполнение формы!')
        return redirect('accounts')
    
def transfer_to_account_page(request):
    """Страничка перевода с счета на счет"""
    context = {
        'title': 'Перевести на счет',
        'transfer_form': TransferToAccountForm(),
    }
    return render(request, 'bookkeeping/transfer_to_account.html', context)

def transfer(request):
    """Перевод на счет"""
    form = TransferToAccountForm(data=request.POST)
    if form.is_valid():
        transfer = form.save(commit=False)
        transfer.user = request.user
        transfer.sum = int(form.cleaned_data['som']) 
        save_transfer_sum(transfer)
        transfer.save()
        return redirect('accounts')
    else:
        messages.error(request, 'Не верное заполнение формы!')
        return redirect('accounts')

class UserIncomesPage(ListView):
    """Страничка доходов пользователя"""
    extra_context = {
        'title': 'Доходы',
    }
    model = UserIncomes
    context_object_name = 'incomes'
    template_name = 'bookkeeping/incomes.html'

    # def get_queryset(self):
    #   """Сортировка по месяцам""" 
    #   pass

    def get_context_data(self):
        """Вывод дополнительных элементов на главную страничку"""
        context = super().get_context_data()
        incomes = UserIncomes.objects.filter(
            user=self.request.user
        )
        context['incomes'] = incomes
        total_sum = get_total_sum_incomes(self.request)
        context['total_sum'] = total_sum
        return context

def add_income_page(request):
    """Страничка добавления дохода"""
    context = {
        'title': 'Добавление дохода',
        'income_form': UserIncomesForm(),
    }
    return render(request, 'bookkeeping/add_income.html', context)

def add_income(request):
    """Добавление"""
    form = UserIncomesForm(data=request.POST)
    if form.is_valid():
        incomes = form.save(commit=False)
        incomes.user = request.user
        save_income_sum(incomes)
        incomes.save()
        return redirect('incomes')
    else:
        messages.error(request, 'Не верное заполнение формы!')
        return redirect('incomes')
    
class UserExpensesPage(ListView):
    """Страничка Расходов пользователя"""
    extra_context = {
        'title': 'Расходы',
    }
    model = UserExpenses
    context_object_name = 'expenses'
    template_name = 'bookkeeping/expenses.html'

    def get_context_data(self):
        """Вывод дополнительных элементов на главную страничку"""
        context = super().get_context_data()
        expenses = UserExpenses.objects.filter(
            user=self.request.user
        )
        context['expenses'] = expenses
        total_sum = get_total_sum_expenses(self.request)
        context['total_sum'] = total_sum
        return context
    
def add_expenses_page(request):
    """Страничка добавления расхода"""
    context = {
        'title': 'Добавление расхода',
        'expenses_form': UserExpensesForm(),
    }
    return render(request, 'bookkeeping/add_expenses.html', context)

def add_expense(request):
    """Добавление расхода"""
    form = UserExpensesForm(data=request.POST)
    if form.is_valid():
        expenses = form.save(commit=False)
        expenses.user = request.user
        save_expenses_sum(expenses)
        expenses.save()
        return redirect('expenses')
    else:
        messages.error(request, 'Не верное заполнение формы!')
        return redirect('expenses')
    


       
