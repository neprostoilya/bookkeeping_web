from datetime import datetime

import plotly.graph_objs as go
from django.shortcuts import get_object_or_404

from .models import UserAccounts, CategoriesCurrencys

def decimal(total_sum):
    """Функция которая возвращает сумму с пробелами"""
    return '{0:,}'.format(int(total_sum)).replace(',', '.')    

def get_total_sum(objects, request):
    """Получение полной суммы"""
    total_sum = sum(
        [_.get_total_sum for _ in objects]
    )
    currencys = []
    for currency in CategoriesCurrencys.objects.filter(user=request.user):
        try:
            currencys.append(f'<strong>{currency.title}:</strong> {decimal(total_sum / currency.course)}')
        except ZeroDivisionError:
            pass
    return currencys
    
def save_transfer_sum(form):
    """Сохранение перевода в базу данных"""
    if form.account1.pk != form.account2.pk:
        account_1 = get_object_or_404(UserAccounts, pk=form.account1.pk)
        account_2 = get_object_or_404(UserAccounts, pk=form.account2.pk)
        transfer_sum1 = int((form.sum * form.currency.course) / form.account1.currency.course)
        account_1.sum = account_1.sum - transfer_sum1
        transfer_sum2 = int((form.sum * form.currency.course) / form.account2.currency.course)
        account_2.sum = account_2.sum + transfer_sum2
        account_1.save()
        account_2.save()

def save_incomes_or_debts_sum(form):
    """Сохранение дохода или возвращение долга в базу данных"""
    account = get_object_or_404(UserAccounts, pk=form.account.pk)
    account_sum = int((form.sum * form.currency.course) / form.account.currency.course)
    account.sum = account.sum + account_sum
    account.save()
    
def save_expenses_or_debts_sum(form):
    """Сохранение расхода или возвращение долга в базу данных"""
    account = get_object_or_404(UserAccounts, pk=form.account.pk)
    account_sum = int((form.sum * form.currency.course) / form.account.currency.course)
    account.sum = account.sum - account_sum
    account.save()

def return_debts_to_account(sum, debts):
    """Возврат деняг на счет"""
    account = get_object_or_404(UserAccounts, pk=debts.account.pk)
    account_sum = int((sum * debts.currency.course) / debts.account.currency.course)
    account.sum = account.sum + account_sum
    account.save()

def return_owe_debts_to_account(sum, owe_debts):
    """Возврат деняг с счета"""
    account = get_object_or_404(UserAccounts, pk=owe_debts.account.pk)
    account_sum = int((sum * owe_debts.currency.course) / owe_debts.account.currency.course)
    account.sum = account.sum - account_sum
    account.save()

def get_total_quantity(object, request):
    """Получение всего колл-ва обьекта"""
    return len(object.objects.filter(
        user=request.user
    ))

def get_month_and_year(request):
    """Получение года и месяца из выбранного списка"""
    date = request.POST.get('date_sel')
    if date:
        date = datetime.strptime(date, '%Y-%m')
        year = date.year
        month = date.month
    else:
        year = month = None
    return year, month

def get_date1_and_date2(request):
    """Получение двух дат из выбранных списков"""
    date_1 = request.POST.get('date_1')
    date_2 = request.POST.get('date_2')
    return date_1, date_2
    