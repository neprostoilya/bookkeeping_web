import plotly.graph_objs as go
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import UserAccount, UserIncomes, UserExpenses, UserDebts, UserOweDebts

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

def save_incomes_or_debts_sum(form):
    """Сохранение дохода или возвращение долга в базу данных"""
    account = get_object_or_404(UserAccount, pk=form.account.pk)
    account_sum = int((form.sum * form.currency.course) / form.account.currency.course)
    account.sum = account.sum + account_sum
    account.save()

def get_total_sum_incomes(request):
    """Получение полной суммы доходов"""
    if request.user.is_authenticated:
        incomes = UserIncomes.objects.filter(
            user=request.user
        )
        total_sum = sum(
            [_.get_total_sum for _ in incomes]
        )
        return decimal(total_sum)  
    else:
        messages.error(request, 'Авторизуйтесь или Зарегистрируйтесь!')
        return redirect('login_registration')
    
def save_expenses_or_debts_sum(form):
    """Сохранение расхода или возвращение долга в базу данных"""
    account = get_object_or_404(UserAccount, pk=form.account.pk)
    account_sum = int((form.sum * form.currency.course) / form.account.currency.course)
    account.sum = account.sum - account_sum
    account.save()

def get_total_sum_expenses(request):
    """Получение полной суммы доходов"""
    if request.user.is_authenticated:
        expenses = UserExpenses.objects.filter(
            user=request.user
        )
        total_sum = sum(
            [_.get_total_sum for _ in expenses]
        )
        return decimal(total_sum)  
    else:
        messages.error(request, 'Авторизуйтесь или Зарегистрируйтесь!')
        return redirect('login_registration')

def get_total_sum_debt(request):
    """Получение полной суммы долгов"""
    if request.user.is_authenticated:
        debts = UserDebts.objects.filter(
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
        debts = UserOweDebts.objects.filter(
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

def graph(list_values, list_keys):
    """Функция для вывода графика"""
    fig = go.Figure()
    pull = [0]*len(list_values)
    pull[list_values.index(max(list_values))] = 0.2
    fig.add_trace(go.Pie(values=list_values, labels=list_keys, pull=pull, hole=0.9))

    fig.update_layout(
        margin=dict(l=50, r=50, b=100, t=100, pad=2),
        legend_orientation="h",
        template='plotly_white'
    )    
    return fig

def graph_income_or_expense(request, title, name_object):
    """Отображение графика дохода и расхода на странице"""
    objects = name_object.objects.all()
    objects_dict = {}
    for object in objects:
        if object.category.title in objects_dict:
            objects_dict[object.category.title + ' - ' + str(object.sum) + ' ' + object.currency.title] += object.get_total_sum
        else:
            objects_dict[object.category.title + ' - ' + str(object.sum) + ' ' + object.currency.title] = object.get_total_sum

    list_values = list(objects_dict.values())
    list_keys = list(objects_dict.keys())

    graphic = graph(list_values, list_keys)

    context = {
        'title': title,
        'graphic': graphic.to_html(full_html=False)
    }
    return render(request, 'bookkeeping/statistics.html', context)

def graph_account(request):
    """Отображение графика счетов на странице"""
    objects = UserAccount.objects.all()
    objects_dict = {}
    for object in objects:
        if object.account.title in objects_dict:
            objects_dict[object.account.title + ' - ' + str(object.sum) + ' ' + object.currency.title ] += object.get_course_sum
        else:
            objects_dict[object.account.title + ' - ' + str(object.sum) + ' ' + object.currency.title] = object.get_course_sum

    list_values = list(objects_dict.values())
    list_keys = list(objects_dict.keys())

    graphic = graph(list_values, list_keys)

    context = {
        'title': 'График счетов',
        'graphic': graphic.to_html(full_html=False)
    }
    return render(request, 'bookkeeping/statistics.html', context)