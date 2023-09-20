from typing import Any, Dict

import base64
import matplotlib.pyplot as plt
from io import BytesIO
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, View
from django.shortcuts import render, redirect, get_object_or_404

from .forms import LoginForm, RegistrationForm, AccountForm, TransferToAccountForm,  \
        UserIncomesForm, UserExpensesForm, UserDebtsForm, UserOweDebtsForm, UserReturnDebtsForm, UserReturnOweDebtsForm
from .models import UserAccount, UserDebt, UserIncomes, UserExpenses, UserOweDebt
from .utils import get_total_sum_account, get_total_sum_debt, get_total_sum_owe_debt, return_debts_to_account, return_owe_debts_to_account, \
save_transfer_sum, save_incomes_or_debts_sum, get_total_sum_incomes, get_total_sum_expenses, save_expenses_or_debts_sum

        
class Page(ListView):
    """Главная страница"""
    extra_context = {
        'title': 'Главная страница',
    }
    template_name = 'bookkeeping/index.html'

    def get_queryset(self):
        pass

# Регистрация и Авторизация

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

# Счета

class UserAccountPage(ListView):
    """Страничка счетов пользователя"""
    extra_context = {
        'title': 'Счета',
    }
    model = UserAccount
    context_object_name = 'accounts'
    template_name = 'bookkeeping/accounts/accounts.html'

    def get_queryset(self):
        """Сортировка в таблице""" 
        accounts = UserAccount.objects.filter(
            user=self.request.user
        ).order_by(
            '?'
        )
        sort_field = self.request.GET.get('sort')
        if sort_field:
            accounts = accounts.order_by(sort_field)
        return accounts[:6]
    
    def get_context_data(self):
        """Вывод дополнительных элементов на главную страничку"""
        context = super().get_context_data()
        context['total_sum'] = get_total_sum_account(self.request)
        return context

class UserAccountUpdate(UpdateView):
    """Редактирование счета"""
    extra_context = {
        'title': 'Изменения счета'
    }
    model = UserAccount
    form_class = AccountForm
    template_name = 'bookkeeping/accounts/update_accounts.html'
    success_url = reverse_lazy('accounts')

def create_account_page(request):
    """Страница создания счета"""
    context = {
        'title': 'Создание счета',
        'form': AccountForm(),
    }
    return render(request, 'bookkeeping/accounts/create_account.html', context)

def create_account(request):
    """Создание счета"""
    form = AccountForm(data=request.POST)
    if form.is_valid():
        account = form.save(commit=False)
        account.user = request.user
        account.save()
        messages.success(request, 'Счет успешно создан!')
        return redirect('accounts')
    else:
        messages.error(request, 'Не верное заполнение формы!')
        return redirect('create_accounts')
    
def transfer_to_account_page(request):
    """Страничка перевода с счета на счет"""
    context = {
        'title': 'Перевести на счет',
        'form': TransferToAccountForm(),
    }
    return render(request, 'bookkeeping/accounts/transfer_to_account.html', context)

def transfer(request):
    """Перевод на счет"""
    form = TransferToAccountForm(data=request.POST)
    if form.is_valid():
        transfer = form.save(commit=False)
        transfer.user = request.user
        save_transfer_sum(transfer)
        transfer.save()
        return redirect('accounts')
    else:
        messages.error(request, 'Не верное заполнение формы!')
        return redirect('transfer_to_account')

def delete_accounts(request):
    """Удаление счетов"""
    if request.method == 'POST':
        selected_pks = request.POST.getlist('selected_action')
        UserAccount.objects.filter(pk__in=selected_pks).delete()
        messages.success(request, 'Выбранные объекты успешно удалены.')
    return redirect('accounts')

# Доходы

class UserIncomesPage(ListView):
    """Страничка доходов пользователя"""
    extra_context = {
        'title': 'Доходы',
    }
    model = UserIncomes
    context_object_name = 'incomes'
    template_name = 'bookkeeping/incomes/incomes.html'

    def get_queryset(self):
        """Сортировка в таблице""" 
        incomes = UserIncomes.objects.filter(
            user=self.request.user
        ).order_by(
            '?'
        )
        sort_field = self.request.GET.get('sort')
        if sort_field:
            incomes = incomes.order_by(sort_field)
        return incomes[:6]

    def get_context_data(self):
        """Вывод дополнительных элементов на главную страничку"""
        context = super().get_context_data()
        total_sum = get_total_sum_incomes(self.request)
        context['total_sum'] = total_sum
        return context

class UserIncomesUpdate(UpdateView):
    """Редактирование дохода"""
    extra_context = {
        'title': 'Изменение дохода'
    }
    model = UserIncomes
    form_class = UserIncomesForm
    template_name = 'bookkeeping/incomes/update_incomes.html'
    success_url = reverse_lazy('incomes')

def add_income_page(request):
    """Страничка добавления дохода"""
    context = {
        'title': 'Добавление дохода',
        'form': UserIncomesForm(),
    }
    return render(request, 'bookkeeping/incomes/add_incomes.html', context)

def add_income(request):
    """Добавление"""
    form = UserIncomesForm(data=request.POST)
    if form.is_valid():
        incomes = form.save(commit=False)
        incomes.user = request.user
        save_incomes_or_debts_sum(incomes)
        incomes.save()
        messages.success(request, 'Доход успешно добавлен!')
        return redirect('incomes')
    else:
        messages.error(request, 'Не верное заполнение формы!')
        return redirect('add_incomes')
    
def delete_incomes(request):
    """Удаление доходов"""
    if request.method == 'POST':
        selected_pks = request.POST.getlist('selected_action')
        UserIncomes.objects.filter(pk__in=selected_pks).delete()
        messages.success(request, 'Выбранные объекты успешно удалены.')
    return redirect('incomes')

# Расходы

class UserExpensesPage(ListView):
    """Страничка Расходов пользователя"""
    extra_context = {
        'title': 'Расходы',
    }
    model = UserExpenses
    context_object_name = 'expenses'
    template_name = 'bookkeeping/expenses/expenses.html'

    def get_queryset(self):
        """Сортировка в таблице""" 
        expenses = UserExpenses.objects.filter(
            user=self.request.user
        ).order_by(
            '?'
        )
        sort_field = self.request.GET.get('sort')
        if sort_field:
            expenses = expenses.order_by(sort_field)
        return expenses[:6] 
    
    def get_context_data(self):
        """Вывод дополнительных элементов на главную страничку"""
        context = super().get_context_data()
        total_sum = get_total_sum_expenses(self.request)
        context['total_sum'] = total_sum
        return context
    
class UserExpensesUpdate(UpdateView):
    """Редактирование расхода"""
    extra_context = {
        'title': 'Изменение расхода'
    }
    model = UserExpenses
    form_class = UserExpensesForm
    template_name = 'bookkeeping/expenses/update_expenses.html'
    success_url = reverse_lazy('expenses')

def add_expenses_page(request):
    """Страничка добавления расхода"""
    context = {
        'title': 'Добавление расхода',
        'form': UserExpensesForm(),
    }
    return render(request, 'bookkeeping/expenses/add_expenses.html', context)

def add_expense(request):
    """Добавление расхода"""
    form = UserExpensesForm(data=request.POST)
    if form.is_valid():
        expenses = form.save(commit=False)
        expenses.user = request.user
        save_expenses_or_debts_sum(expenses)
        expenses.save()
        messages.success(request, 'Расход успешно добавлен!')
        return redirect('expenses')
    else:
        messages.error(request, 'Не верное заполнение формы!')
        return redirect('add_expenses')

def delete_expenses(request):
    """Удаление расходов"""
    if request.method == 'POST':
        selected_pks = request.POST.getlist('selected_action')
        UserExpenses.objects.filter(pk__in=selected_pks).delete()
        messages.success(request, 'Выбранные объекты успешно удалены.')

    return redirect('expenses')

# Долги пользователя

class UserOweDebtsPage(ListView):
    """Страничка Долгов пользователя"""
    extra_context = {
        'title': 'Мои Долги',
    }
    model = UserOweDebt
    context_object_name = 'owe_debts'
    template_name = 'bookkeeping/owe_debts/owe_debts.html'

    def get_queryset(self):
        """Сортировка в таблице""" 
        owe_debts = UserOweDebt.objects.filter(
            user=self.request.user
        ).order_by(
            '?'
        )
        sort_field = self.request.GET.get('sort')
        if sort_field:
            owe_debts = owe_debts.order_by(sort_field)
        return owe_debts[:6]
    
    def get_context_data(self):
        """Вывод дополнительных элементов на главную страничку"""
        context = super().get_context_data()
        context['total_sum'] = get_total_sum_owe_debt(self.request)
        return context

class UserOweDebtsUpdate(UpdateView):
    """Редактирование долга"""
    extra_context = {
        'title': 'Изменение долга'
    }
    model = UserOweDebt
    form_class = UserOweDebtsForm
    template_name = 'bookkeeping/owe_debts/update_owe_debts.html'
    success_url = reverse_lazy('owe_debts')

class UserReturnOweDebts(View):
    """Возврат долга c счета"""
    template_name = 'bookkeeping/owe_debts/return_owe_debts.html'

    def get(self, request, pk):
        owe_debts = get_object_or_404(UserOweDebt, pk=pk)
        form = UserReturnOweDebtsForm()
        return render(request, self.template_name, {
            'title': 'Возврат долга',
            'owe_debts': owe_debts,
            'form': form,
        })
    
    def post(self, request, pk):
        owe_debts = get_object_or_404(UserOweDebt, pk=pk, user=request.user)
        form = UserReturnDebtsForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            return_sum = form.sum
            if 0 <= return_sum <= owe_debts.sum:
                return_owe_debts_to_account(return_sum, owe_debts)
                owe_debts.sum -=  return_sum
                owe_debts.save()
            else:
                return_owe_debts_to_account(owe_debts.sum, owe_debts)
                owe_debts.delete()
            return redirect('owe_debts')
        
        return render(request, self.template_name, {
            'owe_debts': owe_debts,
            'form': form,
        })

def delete_owe_debts(request):
    """Удаление расходов"""
    if request.method == 'POST':
        selected_pks = request.POST.getlist('selected_action')
        UserOweDebt.objects.filter(pk__in=selected_pks).delete()
        messages.success(request, 'Выбранные объекты успешно удалены.')
        redirect('owe_debts')
    else:
        redirect('owe_debts')

def add_owe_debts_page(request):
    """Страничка создания долга"""
    context = {
        'title': 'Добавление долга',
        'form': UserOweDebtsForm(),
    }
    return render(request, 'bookkeeping/owe_debts/add_owe_debts.html', context)

def add_owe_debt(request):
    """Добавление долга"""
    form = UserOweDebtsForm(data=request.POST)
    if form.is_valid():
        owe_debts = form.save(commit=False)
        owe_debts.user = request.user
        owe_debts.initial_sum = owe_debts.sum
        save_incomes_or_debts_sum(owe_debts)
        owe_debts.save()
        messages.success(request, 'Долг успешно добавлен!')
        return redirect('owe_debts')
    else:
        messages.error(request, 'Не верное заполнение формы!')
        return redirect('add_owe_debts')

# Долги у пользователя

class UserDebtsPage(ListView):
    """Страничка Долгов у пользователя"""
    extra_context = {
        'title': 'Долги',
    }
    model = UserDebt
    context_object_name = 'debts'
    template_name = 'bookkeeping/debts/debts.html'

    def get_queryset(self):
        """Сортировка в таблице""" 
        debts = UserDebt.objects.filter(
            user=self.request.user
        ).order_by(
            '?'
        )
        sort_field = self.request.GET.get('sort')
        if sort_field:
            debts = debts.order_by(sort_field)
        return debts[:6]

    def get_context_data(self):
        """Вывод дополнительных элементов на главную страничку"""
        context = super().get_context_data()
        context['total_sum'] = get_total_sum_debt(self.request)
        return context

class UserDebtsUpdate(UpdateView):
    """Редактирование долга"""
    extra_context = {
        'title': 'Изменение долга'
    }
    model = UserDebt
    form_class = UserDebtsForm
    template_name = 'bookkeeping/debts/update_debts.html'
    success_url = reverse_lazy('debts')

class UserReturnDebts(View):
    """Возврат долга на счет"""
    template_name = 'bookkeeping/debts/return_debts.html'

    def get(self, request, pk):
        debts = get_object_or_404(UserDebt, pk=pk)
        form = UserReturnDebtsForm()
        return render(request, self.template_name, {
            'title': 'Возврат долга',
            'debts': debts,
            'form': form,
        })
    
    def post(self, request, pk):
        debts = get_object_or_404(UserDebt, pk=pk, user=request.user)
        form = UserReturnDebtsForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            return_sum = form.sum
            if 0 <= return_sum <= debts.sum:
                return_debts_to_account(return_sum, debts)
                debts.sum -= return_sum
                debts.save()
            else:
                return_debts_to_account(debts.sum, debts)
                debts.delete()
            return redirect('debts')
        
        return render(request, self.template_name, {
            'debts': debts,
            'form': form,
        })

def delete_debts(request):
    """Удаление расходов"""
    if request.method == 'POST':
        selected_pks = request.POST.getlist('selected_action')
        UserDebt.objects.filter(pk__in=selected_pks).delete()
        messages.success(request, 'Выбранные объекты успешно удалены.')
        return redirect('debts')
    else:
        return redirect('debts')

def add_debts_page(request):
    """Страничка создания долга"""
    context = {
        'title': 'Добавление долга',
        'form': UserDebtsForm(),
    }
    return render(request, 'bookkeeping/debts/add_debts.html', context)

def add_debt(request):
    """Добавление долга"""
    form = UserDebtsForm(data=request.POST)
    if form.is_valid():
        debts = form.save(commit=False)
        debts.user = request.user
        debts.initial_sum = debts.sum
        save_expenses_or_debts_sum(debts)
        debts.save()
        messages.success(request, 'Долг успешно добавлен!')
        return redirect('debts')
    else:
        messages.error(request, 'Не верное заполнение формы!')
        return redirect('add_debts')



def statistics(request):
    incomes = UserIncomes.objects.all()
    incomes_dict = {}
    for income in incomes:
        incomes_dict[income.category] = income.sum

    fig, ax = plt.subplots()
    ax.pie(incomes_dict.values(), labels=incomes_dict.keys(), autopct='%1.1f%%')
    ax.set_title('Доходы')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')
    context = {'graphic': graphic}
    return render(request, 'bookkeeping/statistics.html', context)
