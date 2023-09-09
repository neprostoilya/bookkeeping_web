from django import template
from django.template.defaulttags import register as custom_range

register = template.Library() 

@register.simple_tag()
def get_sorted_table():
    """Сортировка по дате и цене"""
    sorters = [
        {
            'title': 'Дата',
            'sorters': [
                ('created_at', '▲'),
                ('-created_at', '▼'),

            ]
        },
        {
            'title': 'Счет',
            'sorters': [
                ('account', '▲'),
                ('-account', '▼'),
            ]
        },
        {
            'title': 'Валюта',
            'sorters': [
                ('currency', '▲'),
                ('-currency', '▼'),

            ]
        },
        {
            'title': 'Сумма',
            'sorters': [
                ('sum', '▲'),
                ('-sum', '▼'),
            ]
        }
    ]
    return sorters

@register.simple_tag()
def get_sorted_table_accounts():
    """Сортировка по курсу и цене"""
    sorters = [
        {
            'title': 'Валюта',
            'sorters': [
                ('currency', '▲'),
                ('-currency', '▼'),

            ]
        },
        {
            'title': 'Сумма',
            'sorters': [
                ('sum', '▲'),
                ('-sum', '▼'),
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
                ('data_1', '▲'),
                ('-data_1', '▼'),

            ]
        },
        {
            'title': 'Дата возврата',
            'sorters': [
                ('data_2', '▲'),
                ('-data_2', '▼'),

            ]
        },
        {
            'title': 'Счет',
            'sorters': [
                ('account', '▲'),
                ('-account', '▼'),
            ]
        },
        {
            'title': 'Валюта',
            'sorters': [
                ('currency', '▲'),
                ('-currency', '▼'),

            ]
        },
        {
            'title': 'Сумма',
            'sorters': [
                ('sum', '▲'),
                ('-sum', '▼'),
            ]
        }
    ]
    return sorters
