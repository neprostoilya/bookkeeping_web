from bookkeeping_site.models import UserAccounts
from conf.celery import task

from .service import graph

@task.task
def graphic_account():
    """График счета"""
    objects = UserAccounts.objects.filter(user='admin')
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
    

@task.task
def graphic_income_or_expense(model, request):
    """График дохода или расхода"""
    # return render_graphic_income_or_expense(model, request)
    pass
    