from django.contrib import messages
from django.shortcuts import redirect

from .models import UserAccount, UserIncomes

def get_total_sum_account(request):
    """Получение полной суммы всех счетов"""
    if request.user.is_authenticated:
        account = UserAccount.objects.filter(
            user=request.user
        )
        total_sum = sum(
            [_.get_course_sum for _ in account]
        )
        return total_sum
    else:
        messages.error(request, 'Авторизуйтесь или Зарегистрируйтесь чтобы совершать покупки!')
        return redirect('login_registration')
    
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
        account_2.sum = account_2.sum + transfer.sum
        account_1.save()
        account_2.save()
    else:
        pass

def save_income_sum(incomes):
    """Сохранение дохода в базу данных"""
    account = UserAccount.objects.get(
        user = incomes.user,
        pk = incomes.account.pk
    )
    account.sum = account.sum + incomes.sum
    account.save()

def get_total_sum_incomes(request):
    """Получение полной суммы доходов"""
    if request.user.is_authenticated:
        incomes = UserIncomes.objects.filter(
            user=request.user
        )
        total_sum = sum(
            [_.sum for _ in incomes]
        )
        return total_sum
    else:
        messages.error(request, 'Авторизуйтесь или Зарегистрируйтесь чтобы совершать покупки!')
        return redirect('login_registration')