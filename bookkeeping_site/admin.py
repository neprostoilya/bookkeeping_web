from django.contrib import admin

from .models import CategoryExpenses, CategoryIncome, CategoryAccounts

@admin.register(CategoryIncome)
class CategoryIncomesAdmin(admin.ModelAdmin):
    """Категории Доходов"""
    list_display = ('pk', 'title', 'parent')
    list_display_links = ('title', 'pk')

@admin.register(CategoryExpenses)
class CategoryExpensesAdmin(admin.ModelAdmin):
    """Категории Расходов"""
    list_display = ('pk', 'title', 'parent')
    list_display_links = ('title', 'pk')

@admin.register(CategoryAccounts)
class CategoryAccountsAdmin(admin.ModelAdmin):
    """Категории Счетов"""
    list_display = ('pk', 'title')
    list_display_links = ('title', 'pk')