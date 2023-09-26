from django import template
from django.template.defaulttags import register as custom_range

register = template.Library() 

@register.simple_tag()
def get_sorted_table():
    """Сортировка таблицы дохода и расхода"""
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
    """Сортировка таблицы счетов"""
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
            'sorters': [
                ('data_1', 'Дата выдачи')
            ]
        },
        {
            'sorters': [
                ('data_2', 'Дата возврата')
            ]
        },
        {
            'sorters': [
                ('account', 'Счет')
            ]
        },
        {
            'sorters': [
                ('comment', 'Коментарий')

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
def get_sorted_table_categories():
    """Сортировка таблицы категорий доходов и расходов"""
    sorters = [
        {
            'sorters': [
                ('title', 'Категория')
            ]
        },
        {
            'sorters': [
                ('parent', 'Подкатегория')

            ]
        }
    ]
    return sorters

@register.simple_tag()
def get_sorted_table_categories_accounts():
    """Сортировка таблицы категорий счетов"""
    sorters = [
        {
            'sorters': [
                ('title', 'Категория')
            ]
        },
    ]
    return sorters

@register.simple_tag()
def get_sorted_table_categories_currencys():
    """Сортировка таблицы категорий счетов"""
    sorters = [
        {
            'sorters': [
                ('title', 'Категория')
            ]
        },
        {
            'sorters': [
                ('course', 'Курс')
            ]
        }
    ]
    return sorters