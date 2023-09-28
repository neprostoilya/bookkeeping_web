import plotly.graph_objs as go

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

def render_graphic_account(model, request):
    """Вывод графика счетов"""
    objects = model.objects.filter(user=request.user)
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

def render_graphic_income_or_expense(model, request):
    """Вывод графика дохода или расхода"""
    objects = model.objects.filter(user=request.user)
    objects_dict = {}
    for object in objects:
        if object.category.title in objects_dict:
            objects_dict[object.category.title + ' - ' + str(object.sum) + ' ' + object.currency.title] += object.get_total_sum
        else:
            objects_dict[object.category.title + ' - ' + str(object.sum) + ' ' + object.currency.title] = object.get_total_sum

    list_values = list(objects_dict.values())
    list_keys = list(objects_dict.keys())

    graphic = graph(list_values, list_keys)
    return graphic

