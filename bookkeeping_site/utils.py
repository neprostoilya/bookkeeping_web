import plotly.graph_objs as go
from django.shortcuts import get_object_or_404, render

from .models import UserAccounts, CategoriesCurrencys

def decimal(total_sum):
    """Функция которая возвращает сумму с пробелами"""
    return '{0:,}'.format(int(total_sum)).replace(',', ' ')    

def get_total_sum(request, object):
    """Получение полной суммы всех счетов"""
    account = object.objects.filter(
        user=request.user
    )
    total_sum = sum(
        [_.get_total_sum for _ in account]
    )
    return total_sum
    
def save_transfer_sum(form):
    """Сохранение перевода в базу данных"""
    if form.account1.pk != form.account2.pk:
        account_1 = get_object_or_404(UserAccounts, pk=form.account1.pk)
        account_2 = get_object_or_404(UserAccounts, pk=form.account2.pk)
        account_1.sum = account_1.sum - form.sum
        transfer_sum2 = int((form.sum * form.account1.currency.course) / form.account2.currency.course)
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

def graph(list_values, list_keys):
    """Функция для вывода графика"""
    if list_values and list_keys:
        fig = go.Figure()
        pull = [0]*len(list_values)
        pull[list_values.index(max(list_values))] = 0.2
        fig.add_trace(go.Pie(values=list_values, labels=list_keys, pull=pull, hole=0.9))

        fig.update_layout(
            margin=dict(l=50, r=50, b=100, t=100, pad=2),
            legend_orientation="h",
            template='plotly_white'
        )    
        return fig.to_html(full_html=False)
    else:
        return None

def graph_income_or_expense(request, title, name_object):
    """Отображение графика дохода и расхода на странице"""
    objects = name_object.objects.filter(user=request.user)
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
        'graphic': graphic
    }
    return render(request, 'bookkeeping/statistics.html', context)

def graph_account(request):
    """Отображение графика счетов на странице"""
    objects = UserAccounts.objects.filter(user=request.user)
    objects_dict = {}
    for object in objects:
        if object.account.title in objects_dict:
            objects_dict[object.account.title + ' - ' + str(object.sum) + ' ' + object.currency.title ] += object.get_total_sum
        else:
            objects_dict[object.account.title + ' - ' + str(object.sum) + ' ' + object.currency.title] = object.get_total_sum

    list_values = list(objects_dict.values())
    list_keys = list(objects_dict.keys())

    graphic = graph(list_values, list_keys)

    context = {
        'title': 'График счетов',
        'graphic': graphic
    }
    return render(request, 'bookkeeping/statistics.html', context)

def get_total_quantity(object, request):
    """Получение всего колл-ва обьекта"""
    return len(object.objects.filter(
        user=request.user
    ))