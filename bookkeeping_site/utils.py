from django.contrib import messages
from django.shortcuts import redirect

from .models import UserAccount

def get_total_sum_account(request):
    """Вывод полной суммы всех счетов"""
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