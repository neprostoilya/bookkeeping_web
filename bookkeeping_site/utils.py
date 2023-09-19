import datetime

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from .models import UserAccount, UserIncomes, UserExpenses, UserDebt, UserOweDebt

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
        account_1 = get_object_or_404(UserAccount, pk=transfer.account1.pk)
        account_2 = get_object_or_404(UserAccount, pk=transfer.account2.pk)
        account_1.sum = account_1.sum - transfer.sum
        transfer_sum2 = int((transfer.sum * transfer.account1.currency.course) / transfer.account2.currency.course)
        account_2.sum = account_2.sum + transfer_sum2
        account_1.save()
        account_2.save()

def save_incomes_or_debts_sum(request):
    """Сохранение дохода или возвращение долга в базу данных"""
    account = get_object_or_404(UserAccount, pk=request.account.pk)
    account_sum = int((request.sum * request.currency.course) / request.account.currency.course)
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
        messages.error(request, 'Авторизуйтесь или Зарегистрируйтесь!')
        return redirect('login_registration')
    
def save_expenses_or_debts_sum(request):
    """Сохранение расхода или возвращение долга в базу данных"""
    account = get_object_or_404(UserAccount, pk=request.account.pk)
    account_sum = int((request.sum * request.currency.course) / request.account.currency.course)
    account.sum = account.sum - account_sum
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
        messages.error(request, 'Авторизуйтесь или Зарегистрируйтесь!')
        return redirect('login_registration')

def get_total_sum_debt(request):
    """Получение полной суммы долгов"""
    if request.user.is_authenticated:
        debts = UserDebt.objects.filter(
            user=request.user
        )
        total_sum = sum(
            [_.get_total_sum_debt for _ in debts]
        )
        return decimal(total_sum)  
    else:
        messages.error(request, 'Авторизуйтесь или Зарегистрируйтесь!')
        return redirect('login_registration')

def get_total_sum_owe_debt(request):
    """Получение полной суммы долгов"""
    if request.user.is_authenticated:
        debts = UserOweDebt.objects.filter(
            user=request.user
        )
        total_sum = sum(
            [_.get_total_sum_owe_debt for _ in debts]
        )
        return decimal(total_sum)  
    else:
        messages.error(request, 'Авторизуйтесь или Зарегистрируйтесь!')
        return redirect('login_registration')

def return_debts_to_account(sum, debts):
    """Возврат деняг на счет"""
    account = get_object_or_404(UserAccount, pk=debts.account.pk)
    account_sum = int((sum * debts.currency.course) / debts.account.currency.course)
    account.sum = account.sum + account_sum
    account.save()

def return_owe_debts_to_account(sum, owe_debts):
    """Возврат деняг с счета"""
    account = get_object_or_404(UserAccount, pk=owe_debts.account.pk)
    account_sum = int((sum * owe_debts.currency.course) / owe_debts.account.currency.course)
    account.sum = account.sum - account_sum
    account.save()