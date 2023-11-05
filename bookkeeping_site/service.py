import datetime
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.shortcuts import get_object_or_404
import plotly.graph_objs as go
import re

from .models import UserAccounts, UserExpenses, UserIncomes

User = get_user_model()

def send_activate_email_message(user_id):
    """Функция отправки письма с подтверждением для аккаунта"""
    user = get_object_or_404(User, id=user_id)
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_url = reverse_lazy('confirm_email', kwargs={'uidb64': uid, 'token': token})
    current_site = Site.objects.get_current().domain
    subject = f'Активируйте свой аккаунт, {user.username}!'
    message = render_to_string('bookkeeping/register/activate_email_send.html', {
        'username': user.username,
        'activation_url': f'http://{current_site}/{activation_url}',
    })
    return user.email_user(subject, message)

def graph(list_values, list_keys):
    """Функция создания графика"""
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

def dont_repeat_yourself(objects):
    """DRY"""
    objects_dict = {}
    for object in objects:
        try:
            if object.subcategory.title:
                if object.subcategory.title in objects_dict:
                    objects_dict[object.subcategory.title] += object.get_total_sum
                else:
                    objects_dict[object.subcategory.title] = object.get_total_sum
        except AttributeError:
            if object.category.title in objects_dict:
                objects_dict[object.category.title] += object.get_total_sum
            else:
                objects_dict[object.category.title] = object.get_total_sum

    list_values = list(objects_dict.values())
    list_keys = list(objects_dict.keys())

    graphic = graph(list_values, list_keys)
    return graphic

def render_graphic_account(user):
    """График счетов"""
    objects = UserAccounts.objects.filter(user=user)
    objects_dict = {}
    for object in objects:
        if object.account.title in objects_dict:
            objects_dict[object.account.title + ' - ' + str(object.sum) + ' ' + object.currency.title ] += object.get_total_sum
        else:
            objects_dict[object.account.title + ' - ' + str(object.sum) + ' ' + object.currency.title] = object.get_total_sum

    list_values = list(objects_dict.values())
    list_keys = list(objects_dict.keys())

    graphic = graph(list_values, list_keys)
    return graphic 

def render_graphic_incomes(user, year, month):
    """График доходов"""
    objects = UserIncomes.objects.filter(
        user=user,  
        created_at__year=year,
        created_at__month=month
    )
    return dont_repeat_yourself(objects)

def render_graphic_expenses(user, year, month):
    """График расходов"""
    objects = UserExpenses.objects.filter(
        user=user,
        created_at__year=year,
        created_at__month=month
    )
    return dont_repeat_yourself(objects)
