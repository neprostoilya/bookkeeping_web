from django import template
from django.template.defaulttags import register as custom_range

register = template.Library() 

@register.simple_tag()
def get_sorted_table():
    """Сортировка по"""
    sorters = [
        {
            'sorters': [
                ('category', 'Категория')
            ]
        },
        {
            'sorters': [
                ('subcategory', 'Подкатегория')
            ]
        },
        {
            'sorters': [
                ('created_at', 'Дата')
            ]
        },
        {
            'sorters': [
                ('comment', 'Коментарий')
            ]
        },
        {
            'sorters': [
                ('account', 'Счет')
            ]
        },
        {
            'sorters': [
                ('currency', 'Валюта')
            ]
        },
        {
            'sorters': [
                ('sum', 'Сумма')
            ]
        }
    ]
    return sorters


@register.simple_tag()
def get_sorted_table_accounts():
    """Сортировка по счетов"""
    sorters = [
        {
            'sorters': [
                ('account', 'Счет')
            ]
        },
        {
            'sorters': [
                ('currency', 'Валюта')
            ]
        },
        {
            'sorters': [
                ('sum', 'Сумма')
            ]
        }
    ]
    return sorters

@register.simple_tag()
def get_sorted_table_debts():
    """Сортировка таблицы долгов"""
    sorters = [
        {
            'title': 'Дата выдачи',
            'sorters': [
                ('data_1',),
                ('-data_1',),

            ]
        },
        {
            'title': 'Дата возврата',
            'sorters': [
                ('data_2',),
                ('-data_2',),

            ]
        },
        {
            'title': 'Счет',
            'sorters': [
                ('account',),
                ('-account',),
            ]
        },
        {
            'title': 'Валюта',
            'sorters': [
                ('currency',),
                ('-currency',),

            ]
        },
        {
            'title': 'Сумма',
            'sorters': [
                ('sum',),
                ('-sum',),
            ]
        }
    ]
    return sorters
