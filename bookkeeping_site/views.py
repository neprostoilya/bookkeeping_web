import base64
from typing import Any, Dict

from django.contrib.auth import login, logout
from django.contrib import messages
from django.forms.models import BaseModelForm
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, View, CreateView, TemplateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .tasks import render_graphic_account_task, send_activate_email_message_task, render_graphic_incomes_task, \
    render_graphic_expenses_task

from .forms import CategoryAccountForm, CategoryCurrencyForm, CategoryExpenseForm, CategoryIncomeForm, LoginForm, \
    RegistrationForm, UserAccountForm, UserDebtForm, UserExpenseForm, UserIncomeForm,  \
    UserOweDebtForm, UserReturnDebtForm, UserReturnOweDebtForm, UserTransferToAccountForm
from .models import CategoriesAccounts, CategoriesCurrencys, CategoriesExpenses, CategoriesIncomes, UserAccounts, UserAccounts, \
    UserDebts, UserIncomes, UserExpenses, UserOweDebts, UserTransferToAccount
from .utils import get_date1_and_date2, get_total_quantity, return_debts_to_account, return_owe_debts_to_account, save_expenses_or_debts_sum, \
    save_transfer_sum, get_total_sum, save_incomes_or_debts_sum, get_month_and_year

User = get_user_model()


# Главная страница

class Page(TemplateView):
    """Главная страница"""
    extra_context = {
        'title': 'Главная страница',
    }
    template_name = 'bookkeeping/index.html'

# Регистрация и Авторизация

def login_authentication(request):
    """Аутендификации пользователя"""
    context = {
        'title': 'Войти',
        'login_form': LoginForm()
    }
    return render(request, 'bookkeeping/register/login_authentication.html', context)

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

class UserRegisterView(CreateView):
    """Страничка регистрации"""
    form_class = RegistrationForm
    success_url = reverse_lazy('index')
    template_name = 'bookkeeping/register/user_register.html'
    extra_context = {
        'title': 'Регистрация на сайте',
    }

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        send_activate_email_message_task.delay(user.id)
        return redirect('email_confirmation_sent')

class UserConfirmEmailView(View):
    """Проверка потдверждения аккаунта"""

    def get(self, request, uidb64, token):
        try:
            uid = base64.b64decode(uidb64+'=').decode('utf-8')
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('email_confirmed')
        else:
            return redirect('email_confirmation_failed')
        
class EmailConfirmationSentView(TemplateView):
    """Страничка отправления письма активации"""
    template_name = 'bookkeeping/register/email_confirmation_sent.html'
    extra_context = {
        'title': 'Письмо активации отправлено',
    }
 
class EmailConfirmedView(TemplateView):
    """Страничка потдвержденого адреса"""
    template_name = 'bookkeeping/register/email_confirmed.html'
    extra_context = {
        'title': 'Ваш электронный адрес активирован!',
    }

class EmailConfirmationFailedView(TemplateView):
    """Страничка не потдвержденого адреса"""
    template_name = 'bookkeeping/register/email_confirmation_failed.html'
    extra_context = {
        'title': 'Ваш электронный адрес не активирован!',
    }
    
# Счета

class AccountPage(LoginRequiredMixin, ListView):
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
        context['total_sum'] = get_total_sum(self.get_queryset())
        return context

class AccountCreate(LoginRequiredMixin, CreateView):
    """Создание счета"""
    extra_context = {
        'title': 'Создание счета'
    }
    model = UserAccounts
    form_class = UserAccountForm
    template_name = 'bookkeeping/accounts/create_account.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        """Если форма валидна"""
        account_form = form.save(commit=False)
        account_form.user = self.request.user
        account_form.save() 
        messages.success(self.request, 'Счет успешно создан!')
        return redirect('accounts')

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении формы!')
        return super().form_invalid(form)

class AccountUpdate(LoginRequiredMixin, UpdateView):
    """Редактирование счета"""
    extra_context = {
        'title': 'Редактирование счета'
    }
    model = UserAccounts
    form_class = UserAccountForm
    template_name = 'bookkeeping/accounts/update_account.html'
    success_url = reverse_lazy('accounts')
    context_object_name = 'account'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form: BaseModelForm):
        """Если форма валидна"""
        messages.success(self.request, 'Счет успешно отредактирован!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении формы!')
        return super().form_invalid(form)

class AccountTransfer(LoginRequiredMixin, CreateView):
    """Перевод счета на счет"""
    extra_context = {
        'title': 'Перевести на счет',
    }
    model = UserTransferToAccount
    form_class = UserTransferToAccountForm
    template_name = 'bookkeeping/accounts/transfer_to_account.html'
    context_object_name = 'account'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
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

class AccountDelete(LoginRequiredMixin, DeleteView):
    """Удаление счета"""
    extra_context = {
        'title': 'Удаление счета'
    }
    model = UserAccounts
    template_name = 'bookkeeping/components/_confirm_delete_account.html'
    success_url = reverse_lazy('accounts')

# Доходы

class IncomePage(LoginRequiredMixin, ListView):
    """Страничка доходов пользователя"""
    extra_context = {
        'title': 'Доходы',
    }
    model = UserIncomes
    context_object_name = 'incomes'
    template_name = 'bookkeeping/incomes/incomes.html'

    def get_queryset(self):
        """Возвращает список доходов пользователя"""
        return self.model.objects.filter(user=self.request.user).order_by('?')

    def post(self, request):
        """Сортировка списка по месяцам и годам"""
        year, month = get_month_and_year(self.request)
        if year and month:
            incomes = self.get_queryset().filter(
                created_at__year=year,
                created_at__month=month
            )
        else:
            incomes = self.get_queryset().order_by('?')

        sort_field = request.GET.get('sort')
        if sort_field:
            incomes = incomes.order_by(sort_field)
        
        context = {
            'title': 'Доходы',
            'incomes': incomes,
            'title': self.extra_context['title']
        }
        return render(self.request, self.template_name, context)

    def get_context_data(self, **kwargs):
        """Вывод дополнительных элементов на гловную страничку"""
        context = super().get_context_data(**kwargs)
        context['total_sum'] = get_total_sum(self.get_queryset())
        return context
    
class IncomeCreate(LoginRequiredMixin, CreateView):
    """Создание дохода"""
    extra_context = {
        'title': 'Создание дохода'
    }
    model = UserIncomes
    form_class = UserIncomeForm
    template_name = 'bookkeeping/incomes/create_income.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
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

class IncomeUpdate(LoginRequiredMixin, UpdateView):
    """Редактирование дохода"""
    extra_context = {
        'title': 'Редактирование дохода'
    }
    model = UserIncomes
    form_class = UserIncomeForm
    template_name = 'bookkeeping/incomes/update_income.html'
    success_url = reverse_lazy('incomes')
    context_object_name = 'income'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form: BaseModelForm):
        """Если форма валидна"""
        messages.success(self.request, 'Доход успешно отредактирован!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении формы!')
        return super().form_invalid(form)

class IncomeDelete(LoginRequiredMixin, DeleteView):
    """Удаление дохода"""
    extra_context = {
        'title': 'Удаление дохода'
    }
    model = UserIncomes
    template_name = 'bookkeeping/components/_confirm_delete.html'
    success_url = reverse_lazy('incomes')

# Расходы

class ExpensePage(LoginRequiredMixin, ListView):
    """Страничка Расходов пользователя"""
    extra_context = {
        'title': 'Расходы',
    }
    model = UserExpenses
    context_object_name = 'expenses'
    template_name = 'bookkeeping/expenses/expenses.html'

    def get_queryset(self):
        """Возвращает список расходов пользователя"""
        return self.model.objects.filter(user=self.request.user).order_by('?')

    def post(self, request):
        """Сортировка списка по месяцам и годам"""
        year, month = get_month_and_year(self.request)
        if year and month:
            expenses = self.get_queryset().filter(
                created_at__year=year,
                created_at__month=month
            )
        else:
            expenses = self.get_queryset().order_by('?')

        sort_field = request.GET.get('sort')
        if sort_field:
            expenses = expenses.order_by(sort_field)
        
        context = {
            'title': self.extra_context['title'],
            'expenses': expenses,
            'total_sum': get_total_sum(expenses)
        }
        return render(self.request, self.template_name, context)

    def get_context_data(self, **kwargs):
        """Вывод дополнительных элементов на главную страничку"""
        context = super().get_context_data(**kwargs)
        context['total_sum'] = get_total_sum(self.get_queryset())
        return context
    
class ExpenseCreate(LoginRequiredMixin, CreateView):
    """Создание расхода"""
    extra_context = {
        'title': 'Создание расхода'
    }
    model = UserExpenses
    form_class = UserExpenseForm
    template_name = 'bookkeeping/expenses/create_expense.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
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

class ExpenseUpdate(LoginRequiredMixin, UpdateView):
    """Редактирование расхода"""
    extra_context = {
        'title': 'Редактирование расхода'
    }
    model = UserExpenses
    form_class = UserExpenseForm
    template_name = 'bookkeeping/expenses/update_expense.html'
    success_url = reverse_lazy('expenses')
    context_object_name = 'expense'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form: BaseModelForm):
        """Если форма валидна"""
        messages.success(self.request, 'Расход успешно отредактирован!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении таблиц!')
        return super().form_invalid(form)

class ExpenseDelete(LoginRequiredMixin, DeleteView):
    """Удаление расхода"""
    extra_context = {
        'title': 'Удаление расхода'
    }
    model = UserExpenses
    template_name = 'bookkeeping/components/_confirm_delete_debts_and_incomes_expenses.html'
    success_url = reverse_lazy('expenses')

# Долги пользователя

class OweDebtPage(LoginRequiredMixin, ListView):
    """Страничка Долгов пользователя"""
    extra_context = {
        'title': 'Мои Долги',
    }
    model = UserOweDebts
    context_object_name = 'owe_debts'
    template_name = 'bookkeeping/owe_debts/owe_debts.html'

    def get_queryset(self):
        """Возвращает список долгов пользователя"""
        return self.model.objects.filter(user=self.request.user).order_by('?')

    def post(self, request):
        """Сортировка списка по месяцам и годам"""
        date_1, date_2 = get_date1_and_date2(self.request)
        if date_1 and date_2:
            owe_debts = self.get_queryset().filter(
                data_1__gte=date_1,
                data_2__lte=date_2
            )
        else:
            owe_debts = self.get_queryset().order_by('?')
        sort_field = request.GET.get('sort')
        if sort_field:
            owe_debts = owe_debts.order_by(sort_field)
        
        context = {
            'title': self.extra_context['title'],
            'owe_debts': owe_debts,
            'total_sum': get_total_sum(owe_debts)
        }
        return render(self.request, self.template_name, context)

    def get_context_data(self, **kwargs):
        """Вывод дополнительных элементов на главную страничку"""
        context = super().get_context_data(**kwargs)
        context['total_sum'] = get_total_sum(self.get_queryset())
        return context
    
class OweDebtCreate(LoginRequiredMixin, CreateView):
    """Создание долга пользователя"""
    extra_context = {
        'title': 'Создание долга'
    }
    model = UserOweDebts
    form_class = UserOweDebtForm
    template_name = 'bookkeeping/owe_debts/create_owe_debt.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
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

class OweDebtUpdate(LoginRequiredMixin, UpdateView):
    """Редактирование долга"""
    extra_context = {
        'title': 'Редактирование долга'
    }
    model = UserOweDebts
    form_class = UserOweDebtForm
    template_name = 'bookkeeping/owe_debts/update_owe_debt.html'
    success_url = reverse_lazy('owe_debts')
    context_object_name = 'owe_debt'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form: BaseModelForm):
        """Если форма валидна"""
        messages.success(self.request, 'Долг успешно отредактирован!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении таблиц!')
        return super().form_invalid(form)

class OweDebtReturn(LoginRequiredMixin, View):
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

class OweDebtDelete(LoginRequiredMixin, DeleteView):
    """Удаление долга пользователя"""
    extra_context = {
        'title': 'Удаление долга'
    }
    model = UserOweDebts
    template_name = 'bookkeeping/components/_confirm_delete_debts_and_incomes_expenses.html'
    success_url = reverse_lazy('owe_debts')

# Долги у пользователя

class DebtPage(LoginRequiredMixin, ListView):
    """Страничка Долгов у пользователя"""
    extra_context = {
        'title': 'Долги',
    }
    model = UserDebts
    context_object_name = 'debts'
    template_name = 'bookkeeping/debts/debts.html'

    def get_queryset(self):
        """Возвращает список долгов у пользователя"""
        return self.model.objects.filter(user=self.request.user).order_by('?')

    def post(self, request):
        """Сортировка списка по месяцам и годам"""
        date_1, date_2 = get_date1_and_date2(self.request)
        if date_1 and date_2:
            owe_debts = self.get_queryset().filter(
                data_1__gte=date_1,
                data_2__lte=date_2
            )
        else:
            owe_debts = self.get_queryset().order_by('?')
        sort_field = request.GET.get('sort')
        if sort_field:
            owe_debts = owe_debts.order_by(sort_field)
        
        context = {
            'title': self.extra_context['title'],
            'debts': owe_debts,
            'total_sum': get_total_sum(owe_debts)
        }
        return render(self.request, self.template_name, context)

    def get_context_data(self, **kwargs):
        """Вывод дополнительных элементов на главную страничку"""
        context = super().get_context_data(**kwargs)    
        context['total_sum'] = get_total_sum(self.get_queryset())
        return context
    
class DebtCreate(LoginRequiredMixin, CreateView):
    """Создание долга у пользователя"""
    extra_context = {
        'title': 'Создание долга'
    }
    model = UserDebts
    form_class = UserDebtForm
    template_name = 'bookkeeping/debts/create_debt.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
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

class DebtUpdate(LoginRequiredMixin, UpdateView):
    """Редактирование долга"""
    extra_context = {
        'title': 'Редактирование долга'
    }
    model = UserDebts
    form_class = UserDebtForm
    template_name = 'bookkeeping/debts/update_debt.html'
    success_url = reverse_lazy('debts')
    context_object_name = 'debt'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form: BaseModelForm):
        """Если форма валидна"""
        messages.success(self.request, 'Долг успешно отредактирован!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении формы!')
        return super().form_invalid(form)

class DebtReturn(LoginRequiredMixin, View):
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

class DebtDelete(LoginRequiredMixin, DeleteView):
    """Удаление долга у пользователя"""
    extra_context = {
        'title': 'Удаление долга'
    }
    model = UserDebts
    template_name = 'bookkeeping/components/_confirm_delete_debts_and_incomes_expenses.html'
    success_url = reverse_lazy('debts')

## График

@login_required
def graph_accounts(request):
    """График счетов"""
    context = {
        'title':'График счетов',
        'graphic': render_graphic_account_task.delay(request.user.pk).get()
    } 
    return render(request, 'bookkeeping/graphic/graphic_account.html', context)
    
#

@login_required
def graph_incomes(request):
    """График доходов"""
    year, month = get_month_and_year(request)
    context = {
        'title':'График доходов',
        'graphic': render_graphic_incomes_task.delay(request.user.pk, year, month).get()
    }
    return render(request, 'bookkeeping/graphic/graphic.html', context)

# 

@login_required
def graph_expenses(request):
    """График расходов"""
    year, month = get_month_and_year(request)
    context = {
        'title':'График расходов',
        'graphic': render_graphic_expenses_task.delay(request.user.pk, year, month).get()
    }
    return render(request, 'bookkeeping/graphic/graphic.html', context)


## Категории 

class CategoryAccountPage(LoginRequiredMixin, ListView):
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

class CategoryAccountCreate(LoginRequiredMixin, CreateView):
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

class CategoryAccountUpdate(LoginRequiredMixin, UpdateView):
    """Редактирование категории счета"""
    extra_context = {
        'title': 'Редактирование категории счета',
    }
    model = CategoriesAccounts
    form_class = CategoryAccountForm
    template_name = 'bookkeeping/categories/categories_accounts/update_category_account.html'
    success_url = reverse_lazy('categories_accounts')
    context_object_name = 'category_account'

    def form_valid(self, form: BaseModelForm):
        """Если форма валидна"""
        messages.success(self.request, 'Категория счета успешно отредактирована!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении таблиц!')
        return super().form_invalid(form)
    
class CategoryAccountDelete(LoginRequiredMixin, DeleteView):
    """Удаление категории счета"""
    extra_context = {
        'title': 'Удаление категории счета'
    }
    model = CategoriesAccounts
    template_name = 'bookkeeping/components/_confirm_delete.html'
    success_url = reverse_lazy('categories_accounts')

#

class CategoryIncomePage(LoginRequiredMixin, ListView):
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

class CategoryIncomeCreate(LoginRequiredMixin, CreateView):
    """Создание категории дохода"""
    extra_context = {
        'title': 'Создание категории дохода',
    }
    model = CategoriesIncomes
    form_class = CategoryIncomeForm
    template_name = 'bookkeeping/categories/categories_incomes/create_category_income.html'
    success_url = reverse_lazy('categories_incomes')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Если форма валидна"""
        category_income_form = form.save(commit=False)
        category_income_form.user = self.request.user
        category_income_form.save() 
        messages.success(self.request, 'Категория дохода успешно создана!')
        return super().form_valid(form)
        
    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении формы!')
        return super().form_invalid(form)
    
class CategoryIncomeUpdate(LoginRequiredMixin, UpdateView):
    """Редактирование категории дохода"""
    extra_context = {
        'title': 'Редактирование категории дохода',
    }
    model = CategoriesIncomes
    form_class = CategoryIncomeForm
    template_name = 'bookkeeping/categories/categories_incomes/update_category_income.html'
    success_url = reverse_lazy('categories_incomes')
    context_object_name = 'category_income'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form: BaseModelForm):
        """Если форма валидна"""
        messages.success(self.request, 'Категория дохода успешно отредактирована!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении таблиц!')
        return super().form_invalid(form)

class CategoryIncomeDelete(LoginRequiredMixin, DeleteView):
    """Удаление категории дохода"""
    extra_context = {
        'title': 'Удаление категории дохода'
    }
    model = CategoriesIncomes
    template_name = 'bookkeeping/components/_confirm_delete.html'
    success_url = reverse_lazy('categories_incomes')

#

class CategoryExpensePage(LoginRequiredMixin, ListView):
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
    
class CategoryExpenseCreate(LoginRequiredMixin, CreateView):
    """Создание категории расхода"""
    extra_context = {
        'title': 'Создание категории расхода',
    }
    model = CategoriesExpenses
    form_class = CategoryExpenseForm
    template_name = 'bookkeeping/categories/categories_expenses/create_category_expense.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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

class CategoryExpenseUpdate(LoginRequiredMixin, UpdateView):
    """Редактирование категории расхода"""
    extra_context = {
        'title': 'Редактирование категории расхода',
    }
    model = CategoriesExpenses
    form_class = CategoryExpenseForm
    template_name = 'bookkeeping/categories/categories_expenses/update_category_expense.html'
    success_url = reverse_lazy('categories_expenses')
    context_object_name = 'category_expense'


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form: BaseModelForm):
        """Если форма валидна"""
        messages.success(self.request, 'Категория расхода успешно отредактирована!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении таблиц!')
        return super().form_invalid(form)

class CategoryExpenseDelete(LoginRequiredMixin, DeleteView):
    """Удаление категории расхода"""
    extra_context = {
        'title': 'Удаление категории расхода'
    }
    model = CategoriesExpenses
    template_name = 'bookkeeping/components/_confirm_delete.html'
    success_url = reverse_lazy('categories_expenses')

# 

class CategoryCurrencyPage(LoginRequiredMixin, ListView):
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

class CategoryCurrencyCreate(LoginRequiredMixin, CreateView):
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

class CategoryCurrencyUpdate(LoginRequiredMixin, UpdateView):
    """Редактирование категории валюты"""
    extra_context = {
        'title': 'Редактирование категории валюты',
    }
    model = CategoriesCurrencys
    form_class = CategoryCurrencyForm
    template_name = 'bookkeeping/categories/categories_currencys/update_category_currency.html'
    success_url = reverse_lazy('categories_currencys')
    context_object_name = 'category_currency'

    def form_valid(self, form: BaseModelForm):
        """Если форма валидна"""
        messages.success(self.request, 'Категория валюты успешно отредактирована!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Если форма не валидна"""
        messages.error(self.request, 'Ошибка в заполнении таблиц!')
        return super().form_invalid(form)

class CategoryCurrencyDelete(LoginRequiredMixin, DeleteView):
    """Удаление категории валюты"""
    extra_context = {
        'title': 'Удаление категории валюты'
    }
    model = CategoriesCurrencys
    template_name = 'bookkeeping/components/_confirm_delete.html'
    success_url = reverse_lazy('categories_currencys')