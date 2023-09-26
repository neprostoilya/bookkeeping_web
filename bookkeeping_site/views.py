from typing import Any, Dict

from django.contrib.auth import login, logout
from django.contrib import messages
from django.forms.models import BaseModelForm
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, View, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import CategoryAccountForm, CategoryCurrencyForm, CategoryExpenseForm, CategoryIncomeForm, LoginForm, \
    RegistrationForm, UserAccountForm, UserDebtForm, UserExpenseForm, UserIncomeForm, \
    UserOweDebtForm, UserReturnDebtForm, UserReturnOweDebtForm, UserTransferToAccountForm
from .models import CategoriesAccounts, CategoriesCurrencys, CategoriesExpenses, CategoriesIncomes, UserAccounts, UserAccounts, \
    UserDebts, UserIncomes, UserExpenses, UserOweDebts, UserTransferToAccount
from .utils import get_total_quantity, return_debts_to_account, return_owe_debts_to_account, save_expenses_or_debts_sum, \
    save_transfer_sum, get_total_sum, graph_income_or_expense, graph_account, save_incomes_or_debts_sum


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

@method_decorator(login_required, name='dispatch')
class AccountPage(ListView):
    """Страничка счетов пользователя"""
    extra_context = {
        'title': 'Счета',
    }
    model = UserAccounts
    context_object_name = 'accounts'
    template_name = 'bookkeeping/accounts/accounts.html'

    def get_queryset(self):
        """Сортировка в таблице""" 
        accounts = UserAccounts.objects.filter(
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
        context['total_sum'] = get_total_sum(self.request, self.model)
        context['total_quantity'] = get_total_quantity(self.model, self.request) 
        return context

@method_decorator(login_required, name='dispatch')
class AccountCreate(CreateView):
    """Создание счета"""
    extra_context = {
        'title': 'Создание счета'
    }
    model = UserAccounts
    form_class = UserAccountForm
    template_name = 'bookkeeping/accounts/create_account.html'

    def form_valid(self, form):
        """Если форма валидна"""
        account_form = form.save(commit=False)
        account_form.user = self.request.user
        account_form.save() 
        messages.success(self.request, 'Счет успешно создан!')
        return redirect('accounts')

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении таблиц!')
        return super().form_invalid(form)

@method_decorator(login_required, name='dispatch')
class AccountUpdate(UpdateView):
    """Редактирование счета"""
    extra_context = {
        'title': 'Редактирование счета'
    }
    model = UserAccounts
    form_class = UserAccountForm
    template_name = 'bookkeeping/accounts/update_account.html'
    success_url = reverse_lazy('accounts')
    
    def form_valid(self, form: BaseModelForm):
        """Если форма валидна"""
        messages.success(self.request, 'Счет успешно отредактирован!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении таблиц!')
        return super().form_invalid(form)

@method_decorator(login_required, name='dispatch')
class TransferToAccount(CreateView):
    """Перевод счета на счет"""
    extra_context = {
        'title': 'Перевести на счет',
    }
    model = UserTransferToAccount
    form_class = UserTransferToAccountForm
    template_name = 'bookkeeping/accounts/transfer_to_account.html'

    def form_valid(self, form):
        """Если форма валидна"""
        transfer_form = form.save(commit=False)
        transfer_form.user = self.request.user
        save_transfer_sum(transfer_form)
        transfer_form.save()
        messages.success(self.request, 'Перевод успешно переведен!')
        return redirect('accounts')

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении формы!')
        return super().form_invalid(form)

@login_required
def graph_accounts(request):
    """График счетов"""
    return graph_account(request)

@login_required
def delete_accounts(request):
    """Удаление счетов"""
    if request.method == 'POST':
        selected_pks = request.POST.getlist('selected_action')
        UserAccount.objects.filter(pk__in=selected_pks).delete()
        messages.success(request, 'Выбранные объекты успешно удалены.')
    return redirect('accounts')

# Доходы

@method_decorator(login_required, name='dispatch')
class IncomePage(ListView):
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
        context['total_sum'] = get_total_sum(self.request, self.model)
        context['total_quantity'] = get_total_quantity(self.model, self.request) 
        return context

@method_decorator(login_required, name='dispatch')
class IncomeCreate(CreateView):
    """Создание дохода"""
    extra_context = {
        'title': 'Создание дохода'
    }
    model = UserIncomes
    form_class = UserIncomeForm
    template_name = 'bookkeeping/incomes/create_income.html'

    def form_valid(self, form):
        """Если форма валидна"""
        incomes_form = form.save(commit=False)
        incomes_form.user = self.request.user
        save_incomes_or_debts_sum(incomes_form)
        incomes_form.save() 
        messages.success(self.request, 'Доход успешно создан!')
        return redirect('incomes')

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении формы!')
        return super().form_invalid(form)

@method_decorator(login_required, name='dispatch')
class IncomeUpdate(UpdateView):
    """Редактирование дохода"""
    extra_context = {
        'title': 'Редактирование дохода'
    }
    model = UserIncomes
    form_class = UserIncomeForm
    template_name = 'bookkeeping/incomes/update_income.html'
    success_url = reverse_lazy('incomes')

    def form_valid(self, form: BaseModelForm):
        """Если форма валидна"""
        messages.success(self.request, 'Доход успешно отредактирован!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении формы!')
        return super().form_invalid(form)

@login_required
def graph_incomes(request):
    """График доходов"""
    return graph_income_or_expense(request, 'График Доходов', UserIncomes)
    
@login_required    
def delete_incomes(request):
    """Удаление доходов"""
    if request.method == 'POST':
        selected_pks = request.POST.getlist('selected_action')
        UserIncomes.objects.filter(pk__in=selected_pks).delete()
        messages.success(request, 'Выбранные объекты успешно удалены.')
    return redirect('incomes')

# Расходы

@method_decorator(login_required, name='dispatch')
class ExpensePage(ListView):
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
        context['total_sum'] = get_total_sum(self.request, self.model)
        context['total_quantity'] = get_total_quantity(self.model, self.request) 
        return context

@method_decorator(login_required, name='dispatch')
class ExpenseCreate(CreateView):
    """Создание расхода"""
    extra_context = {
        'title': 'Создание расхода'
    }
    model = UserExpenses
    form_class = UserExpenseForm
    template_name = 'bookkeeping/expenses/create_expense.html'

    def form_valid(self, form):
        """Если форма валидна"""
        expense_form = form.save(commit=False)
        expense_form.user = self.request.user
        save_expenses_or_debts_sum(expense_form)
        expense_form.save() 
        messages.success(self.request, 'Расход успешно создан!')
        return redirect('expenses')
    
    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении таблиц!')
        return super().form_invalid(form) 

@method_decorator(login_required, name='dispatch')
class ExpenseUpdate(UpdateView):
    """Редактирование расхода"""
    extra_context = {
        'title': 'Редактирование расхода'
    }
    model = UserExpenses
    form_class = UserExpenseForm
    template_name = 'bookkeeping/expenses/update_expense.html'
    success_url = reverse_lazy('expenses')

    def form_valid(self, form: BaseModelForm):
        """Если форма валидна"""
        messages.success(self.request, 'Расход успешно отредактирован!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении таблиц!')
        return super().form_invalid(form)

@login_required
def graph_expenses(request):
    """График расходов"""
    return graph_income_or_expense(request, 'График Расходов', UserExpenses)

@login_required
def delete_expenses(request):
    """Удаление расходов"""
    if request.method == 'POST':
        selected_pks = request.POST.getlist('selected_action')
        UserExpenses.objects.filter(pk__in=selected_pks).delete()
        messages.success(request, 'Выбранные объекты успешно удалены.')

    return redirect('expenses')

# Долги пользователя

@method_decorator(login_required, name='dispatch')
class OweDebtPage(ListView):
    """Страничка Долгов пользователя"""
    extra_context = {
        'title': 'Мои Долги',
    }
    model = UserOweDebts
    context_object_name = 'owe_debts'
    template_name = 'bookkeeping/owe_debts/owe_debts.html'

    def get_queryset(self):
        """Сортировка в таблице""" 
        owe_debts = UserOweDebts.objects.filter(
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
        context['total_sum'] = get_total_sum(self.request, self.model)
        context['total_quantity'] = get_total_quantity(self.model, self.request) 
        return context

@method_decorator(login_required, name='dispatch')
class OweDebtCreate(CreateView):
    """Создание долга пользователя"""
    extra_context = {
        'title': 'Создание долга'
    }
    model = UserOweDebts
    form_class = UserOweDebtForm
    template_name = 'bookkeeping/owe_debts/create_owe_debt.html'

    def form_valid(self, form):
        """Если форма валидна"""
        owe_debt_form = form.save(commit=False)
        owe_debt_form.user = self.request.user
        owe_debt_form.initial_sum = owe_debt_form.sum
        save_incomes_or_debts_sum(owe_debt_form)
        owe_debt_form.save() 
        messages.success(self.request, 'Долг успешно создан!')
        return redirect('owe_debts')

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении формы!')
        return super().form_invalid(form)

@method_decorator(login_required, name='dispatch')
class OweDebtUpdate(UpdateView):
    """ долга"""
    extra_context = {
        'title': 'Редактирование долга'
    }
    model = UserOweDebts
    form_class = UserOweDebtForm
    template_name = 'bookkeeping/owe_debts/update_owe_debt.html'
    success_url = reverse_lazy('owe_debts')

    def form_valid(self, form: BaseModelForm):
        """Если форма валидна"""
        messages.success(self.request, 'Долг успешно отредактирован!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении таблиц!')
        return super().form_invalid(form)

@method_decorator(login_required, name='dispatch')
class OweDebtReturn(View):
    """Возврат долга c счета"""
    template_name = 'bookkeeping/owe_debts/return_owe_debt.html'

    def get(self, request, pk):
        owe_debts = get_object_or_404(UserOweDebts, pk=pk)
        form = UserReturnOweDebtForm()
        return render(request, self.template_name, {
            'title': 'Возврат долга',
            'owe_debts': owe_debts,
            'form': form,
        })
    
    def post(self, request, pk):
        owe_debts = get_object_or_404(UserOweDebts, pk=pk, user=request.user)
        form = UserReturnOweDebtForm(request.POST)

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
            messages.success(self.request, 'Долг успешно возвращен!')
            return redirect('owe_debts')
        
        return render(request, self.template_name, {
            'owe_debts': owe_debts,
            'form': form,
        })

@login_required
def delete_owe_debts(request):
    """Удаление долгов пользователя"""
    if request.method == 'POST':
        selected_pks = request.POST.getlist('selected_action')
        UserOweDebts.objects.filter(pk__in=selected_pks).delete()
        messages.success(request, 'Выбранные объекты успешно удалены.')
    redirect('owe_debts')

# Долги у пользователя

@method_decorator(login_required, name='dispatch')
class DebtPage(ListView):
    """Страничка Долгов у пользователя"""
    extra_context = {
        'title': 'Долги',
    }
    model = UserDebts
    context_object_name = 'debts'
    template_name = 'bookkeeping/debts/debts.html'

    def get_queryset(self):
        """Сортировка в таблице""" 
        debts = UserDebts.objects.filter(
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
        context['total_sum'] = get_total_sum(self.request, self.model)
        context['total_quantity'] = get_total_quantity(self.model, self.request) 
        return context

@method_decorator(login_required, name='dispatch')
class DebtCreate(CreateView):
    """Создание долга у пользователя"""
    extra_context = {
        'title': 'Создание долга'
    }
    model = UserDebts
    form_class = UserDebtForm
    template_name = 'bookkeeping/debts/create_debt.html'

    def form_valid(self, form):
        """Проверка на валидность"""
        debt_form = form.save(commit=False)
        debt_form.user = self.request.user
        debt_form.initial_sum = debt_form.sum
        save_expenses_or_debts_sum(debt_form)
        debt_form.save() 
        messages.success(self.request, 'Долг успешно создан!')
        return redirect('debts')

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка в заполнении формы!')
        return super().form_invalid(form)

@method_decorator(login_required, name='dispatch')
class DebtUpdate(UpdateView):
    """Редактирование долга"""
    extra_context = {
        'title': 'Редактирование долга'
    }
    model = UserDebts
    form_class = UserDebtForm
    template_name = 'bookkeeping/debts/update_debt.html'
    success_url = reverse_lazy('debts')

    def form_valid(self, form: BaseModelForm):
        """Если форма валидна"""
        messages.success(self.request, 'Долг успешно отредактирован!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении формы!')
        return super().form_invalid(form)

@method_decorator(login_required, name='dispatch')
class DebtReturn(View):
    """Возврат долга на счет"""
    template_name = 'bookkeeping/debts/return_debt.html'

    def get(self, request, pk):
        debts = get_object_or_404(UserDebts, pk=pk)
        form = UserReturnDebtForm()
        return render(request, self.template_name, {
            'title': 'Возврат долга',
            'debts': debts,
            'form': form,
        })
    
    def post(self, request, pk):
        debts = get_object_or_404(UserDebts, pk=pk, user=request.user)
        form = UserReturnDebtForm(request.POST)

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
            messages.success(self.request, 'Долг успешно возвращен!')
            return redirect('debts')
        
        return render(request, self.template_name, {
            'debts': debts,
            'form': form,
        })

@login_required
def delete_debts(request):
    """Удаление расходов"""
    if request.method == 'POST':
        selected_pks = request.POST.getlist('selected_action')
        UserDebts.objects.filter(pk__in=selected_pks).delete()
        messages.success(request, 'Выбранные объекты успешно удалены.')
    return redirect('debts')

## Категории 

#

@method_decorator(login_required, name='dispatch')
class CategoryAccountPage(ListView):
    """Страничка Категорий счета"""
    extra_context = {
        'title': 'Категории Счетов',
    }
    model = CategoriesAccounts
    context_object_name = 'categories'
    template_name = 'bookkeeping/categories/categories_accounts/categories_accounts.html'

    def get_queryset(self):
        categories = self.model.objects.filter(
            user=self.request.user
        ).order_by(
            '?'
        )
        sort_field = self.request.GET.get('sort')
        if sort_field:
            categories = categories.order_by(sort_field)
        return categories 

    def get_context_data(self):
        """Вывод дополнительных элементов на главную страничку"""
        context = super().get_context_data()
        context['total_quantity'] = get_total_quantity(self.model, self.request) 
        return context

@method_decorator(login_required, name='dispatch')
class CategoryAccountCreate(CreateView):
    """Создание категории счета"""
    extra_context = {
        'title': 'Создание категории счета',
    }
    model = CategoriesAccounts
    form_class = CategoryAccountForm
    template_name = 'bookkeeping/categories/categories_accounts/create_category_account.html'

    def form_valid(self, form):
        """Если форма валидна"""
        category_account_form = form.save(commit=False)
        category_account_form.user = self.request.user
        category_account_form.save() 
        messages.success(self.request, 'Категория счета успешно создана!')
        return redirect('categories_accounts')
    
    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении формы!')
        return super().form_invalid(form)

@method_decorator(login_required, name='dispatch')
class CategoryAccountUpdate(UpdateView):
    """Редактирование категории счета"""
    extra_context = {
        'title': 'Редактирование категории счета',
    }
    model = CategoriesAccounts
    form_class = CategoryAccountForm
    template_name = 'bookkeeping/categories/categories_accounts/update_category_account.html'
    success_url = reverse_lazy('categories_accounts')

    def form_valid(self, form: BaseModelForm):
        """Если форма валидна"""
        messages.success(self.request, 'Категория счета успешно отредактирована!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении таблиц!')
        return super().form_invalid(form)
    
@login_required
def delete_categories_accounts(request):
    """Удаление категорий счетов"""
    if request.method == 'POST':
        selected_pks = request.POST.getlist('selected_action')
        CategoriesAccounts.objects.filter(pk__in=selected_pks).delete()
        messages.success(request, 'Выбранные объекты успешно удалены.')
    return redirect('categories_accounts')

#

@method_decorator(login_required, name='dispatch')
class CategoryIncomePage(ListView):
    """Страничка Категорий дохода"""
    extra_context = {
        'title': 'Категории доходов',
    }
    model = CategoriesIncomes
    context_object_name = 'categories'
    template_name = 'bookkeeping/categories/categories_incomes/categories_incomes.html'

    def get_queryset(self):
        categories = self.model.objects.filter(
            user=self.request.user
        ).order_by(
            '?'
        )
        sort_field = self.request.GET.get('sort')
        if sort_field:
            categories = categories.order_by(sort_field)
        return categories 

    def get_context_data(self):
        """Вывод дополнительных элементов на главную страничку"""
        context = super().get_context_data()
        context['total_quantity'] = get_total_quantity(self.model, self.request) 
        return context

@method_decorator(login_required, name='dispatch')
class CategoryIncomeCreate(CreateView):
    """Создание категории дохода"""
    extra_context = {
        'title': 'Создание категории дохода',
    }
    model = CategoriesIncomes
    form_class = CategoryIncomeForm
    template_name = 'bookkeeping/categories/categories_incomes/create_category_income.html'

    def form_valid(self, form):
        """Если форма валидна"""
        category_income_form = form.save(commit=False)
        category_income_form.user = self.request.user
        category_income_form.save() 
        messages.success(self.request, 'Категория дохода успешно создана!')
        return redirect('categories_incomes')
    
    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении формы!')
        return super().form_invalid(form)

@method_decorator(login_required, name='dispatch')
class CategoryIncomeUpdate(UpdateView):
    """Редактирование категории дохода"""
    extra_context = {
        'title': 'Редактирование категории дохода',
    }
    model = CategoriesIncomes
    form_class = CategoryIncomeForm
    template_name = 'bookkeeping/categories/categories_incomes/update_category_income.html'
    success_url = reverse_lazy('categories_incomes')

    def form_valid(self, form: BaseModelForm):
        """Если форма валидна"""
        messages.success(self.request, 'Категория дохода успешно отредактирована!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении таблиц!')
        return super().form_invalid(form)

@login_required
def delete_categories_incomes(request):
    """Удаление категорий доходов"""
    if request.method == 'POST':
        selected_pks = request.POST.getlist('selected_action')
        CategoriesIncomes.objects.filter(pk__in=selected_pks).delete()
        messages.success(request, 'Выбранные объекты успешно удалены.')
    return redirect('categories_incomes')

#

@method_decorator(login_required, name='dispatch')
class CategoryExpensePage(ListView):
    """Страничка Категорий расхода"""
    extra_context = {
        'title': 'Категории расходов',
    }
    model = CategoriesExpenses
    context_object_name = 'categories'
    template_name = 'bookkeeping/categories/categories_expenses/categories_expenses.html'

    def get_queryset(self):
        categories = self.model.objects.filter(
            user=self.request.user
        ).order_by(
            '?'
        )
        sort_field = self.request.GET.get('sort')
        if sort_field:
            categories = categories.order_by(sort_field)
        return categories 
    
    def get_context_data(self):
        """Вывод дополнительных элементов на главную страничку"""
        context = super().get_context_data()
        context['total_quantity'] = get_total_quantity(self.model, self.request) 
        return context
    
@method_decorator(login_required, name='dispatch')
class CategoryExpenseCreate(CreateView):
    """Создание категории расхода"""
    extra_context = {
        'title': 'Создание категории расхода',
    }
    model = CategoriesExpenses
    form_class = CategoryExpenseForm
    template_name = 'bookkeeping/categories/categories_expenses/create_category_expense.html'

    def form_valid(self, form):
        """Если форма валидна"""
        category_expense_form = form.save(commit=False)
        category_expense_form.user = self.request.user
        category_expense_form.save() 
        messages.success(self.request, 'Категория расхода успешно создана!')
        return redirect('categories_expenses')
    
    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении формы!')
        return super().form_invalid(form)

@method_decorator(login_required, name='dispatch')
class CategoryExpenseUpdate(UpdateView):
    """Редактирование категории расхода"""
    extra_context = {
        'title': 'Редактирование категории расхода',
    }
    model = CategoriesExpenses
    form_class = CategoryExpenseForm
    template_name = 'bookkeeping/categories/categories_expenses/update_category_expense.html'
    success_url = reverse_lazy('categories_expenses')

    def form_valid(self, form: BaseModelForm):
        """Если форма валидна"""
        messages.success(self.request, 'Категория расхода успешно отредактирована!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении таблиц!')
        return super().form_invalid(form)

@login_required
def delete_categories_expenses(request):
    """Удаление категорий расходов"""
    if request.method == 'POST':
        selected_pks = request.POST.getlist('selected_action')
        CategoriesExpenses.objects.filter(pk__in=selected_pks).delete()
        messages.success(request, 'Выбранные объекты успешно удалены.')
    return redirect('categories_expenses')

# 

@method_decorator(login_required, name='dispatch')
class CategoryCurrencyPage(ListView):
    """Страничка Категорий валюты"""

    extra_context = {
        'title': 'Категории валют',
    }
    model = CategoriesCurrencys
    context_object_name = 'categories'
    template_name = 'bookkeeping/categories/categories_currencys/categories_currencys.html'

    def get_queryset(self):
        categories = self.model.objects.filter(
            user=self.request.user
        ).order_by(
            '?'
        )
        sort_field = self.request.GET.get('sort')
        if sort_field:
            categories = categories.order_by(sort_field)
        return categories 
    
    def get_context_data(self):
        """Вывод дополнительных элементов на главную страничку"""
        context = super().get_context_data()
        context['total_quantity'] = get_total_quantity(self.model, self.request) 
        return context

@method_decorator(login_required, name='dispatch')
class CategoryCurrencyCreate(CreateView):
    """Создание категории валюты"""
    extra_context = {
        'title': 'Создание категории валюты',
    }
    model = CategoriesCurrencys
    form_class = CategoryCurrencyForm
    template_name = 'bookkeeping/categories/categories_currencys/create_category_currency.html'

    def form_valid(self, form):
        """Если форма валидна"""
        category_currency_form = form.save(commit=False)
        category_currency_form.user = self.request.user
        category_currency_form.save() 
        messages.success(self.request, 'Категория валюты успешно создана!')
        return redirect('categories_currencys')
    
    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении формы!')
        return super().form_invalid(form)

@method_decorator(login_required, name='dispatch')
class CategoryCurrencyUpdate(UpdateView):
    """Редактирование категории валюты"""
    extra_context = {
        'title': 'Редактирование категории валюты',
    }
    model = CategoriesCurrencys
    form_class = CategoryCurrencyForm
    template_name = 'bookkeeping/categories/categories_currencys/update_category_currency.html'
    success_url = reverse_lazy('categories_currencys')

    def form_valid(self, form: BaseModelForm):
        """Если форма валидна"""
        messages.success(self.request, 'Категория валюты успешно отредактирована!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении таблиц!')
        return super().form_invalid(form)

@login_required
def delete_categories_currencys(request):
    """Удаление категорий валют"""
    if request.method == 'POST':
        selected_pks = request.POST.getlist('selected_action')
        CategoriesCurrencys.objects.filter(pk__in=selected_pks).delete()
        messages.success(request, 'Выбранные объекты успешно удалены.')
    return redirect('categories_currencys')

