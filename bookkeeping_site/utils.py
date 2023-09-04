import datetime

from django.contrib import messages
from django.shortcuts import redirect

from .models import UserAccount, UserIncomes, UserExpenses, UserDebt

def decimal(total_sum):
    """Функция которая возвращает сумму с пробелами"""
    return '{0:,}'.format(int(total_sum)).replace(',', ' ')    

def get_total_sum_account(request):
    """Получение полной суммы всех счетов"""
    account = UserAccount.objects.filter(
        user=request.user
    )
    total_sum = sum(
        [_.get_course_sum for _ in account]
    )
    total_sum = '{0:,}'.format(int(total_sum)).replace(',', ' ')
    return total_sum
    
def save_transfer_sum(transfer):
    """Сохранение перевода в базу данных"""
    if transfer.account1.pk != transfer.account2.pk:
        account_1 = UserAccount.objects.get(
            user = transfer.user,
            pk = transfer.account1.pk
        )
        account_2 = UserAccount.objects.get(
            user = transfer.user,
            pk = transfer.account2.pk
        )
        account_1.sum = account_1.sum - transfer.sum
        transfer_sum2 = int((transfer.sum * transfer.account1.currency.course) / transfer.account2.currency.course)
        account_2.sum = account_2.sum + transfer_sum2
        account_1.save()
        account_2.save()
    else:
        pass

def save_incomes_or_debts_sum(object):
    """Сохранение дохода или возвращение долга в базу данных"""
    account = UserAccount.objects.get(
        user = object.user,
        pk = object.account.pk
    )
    account_sum = int((object.sum * object.currency.course) / object.account.currency.course)
    account.sum = account.sum + account_sum
    account.save()

def get_total_sum_incomes(request):
    """Получение полной суммы доходов"""
    if request.user.is_authenticated:
        incomes = UserIncomes.objects.filter(
            user=request.user
        )
        total_sum = sum(
            [_.get_total_sum_income for _ in incomes]
        )
        return decimal(total_sum)  
    else:
        messages.error(request, 'Авторизуйтесь или Зарегистрируйтесь чтобы совершать покупки!')
        return redirect('login_registration')
    
def save_expenses_or_debts_sum(object):
    """Сохранение расхода или возвращение долга в базу данных"""
    account = UserAccount.objects.get(
        user = object.user,
        pk = object.account.pk
    )
    account_sum = int((object.sum * object.currency.course) / object.account.currency.course)
    account.sum = account.sum + account_sum
    account.save()

def get_total_sum_expenses(request):
    """Получение полной суммы доходов"""
    if request.user.is_authenticated:
        expenses = UserExpenses.objects.filter(
            user=request.user
        )
        total_sum = sum(
            [_.get_total_sum_expenses for _ in expenses]
        )
        return decimal(total_sum)  
    else:
        messages.error(request, 'Авторизуйтесь или Зарегистрируйтесь чтобы совершать покупки!')
        return redirect('login_registration')

