from django.contrib import admin

from .models import CategoriesExpenses, CategoriesIncomes, CategoriesCurrencys, UserDebts,  UserOweDebts, \
                    UserExpenses, UserIncomes, UserAccounts, CategoriesAccounts, UserTransferToAccount

@admin.register(CategoriesIncomes)
class CategoryIncomesAdmin(admin.ModelAdmin):
    """Категории Доходов"""
    list_display = ('pk', 'user', 'title', 'subcategory')
    list_display_links = ('title', 'pk')

@admin.register(CategoriesExpenses)
class CategoryExpensesAdmin(admin.ModelAdmin):
    """Категории Расходов"""
    list_display = ('pk', 'user', 'title', 'subcategory')
    list_display_links = ('title', 'pk')

@admin.register(CategoriesCurrencys)
class CategoryCurrencyAdmin(admin.ModelAdmin):
    """Категории валют"""
    list_display = ('pk', 'user', 'title', 'course')
    list_display_links = ('title', 'pk')

@admin.register(UserExpenses)
class UserExpensesAdmin(admin.ModelAdmin):
    """Расходы пользователя"""
    list_display = ('pk', 'user', 'category', 'account', 'created_at', 'currency', 'sum')
    list_filter = ('created_at', 'sum',)
    list_editable = ('sum', 'currency')
    list_display_links = ('user', 'pk')
    
@admin.register(UserIncomes)
class UserIncomesAdmin(admin.ModelAdmin):
    """Доходы пользователя"""
    list_display = ('pk', 'user', 'category', 'account', 'created_at', 'currency', 'sum')
    list_filter = ('created_at', 'sum',)
    list_editable = ('sum', 'currency')
    list_display_links = ('user', 'pk')

@admin.register(UserAccounts)
class UserAccountAdmin(admin.ModelAdmin):
    """Счета пользователя"""
    list_display = ('pk', 'user', 'account', 'currency', 'sum')
    list_filter = ('sum',)
    list_display_links = ('user', 'pk')

@admin.register(CategoriesAccounts)
class CategoryAccountsAdmin(admin.ModelAdmin):
    """Категории Счетов"""
    list_display = ('pk', 'user', 'title')
    list_editable = ('title',)

@admin.register(UserTransferToAccount)
class UserTransferToAccountAdmin(admin.ModelAdmin):
    """Переводы пользователей"""
    list_display = ('pk', 'user', 'account1', 'account2', 'sum')
    list_filter = ('sum',)
    list_display_links = ('user', 'pk')

@admin.register(UserOweDebts)
class UserOweDebtAdmin(admin.ModelAdmin):
    """Долги y пользователей"""
    list_display = ('pk', 'user', 'name', 'data_1', 'data_2', 'account', 'comment', 'currency', 'sum', 'initial_sum')
    list_filter = ('sum', 'data_1', 'data_2')
    list_display_links = ('user', 'pk', 'name')

@admin.register(UserDebts)
class UserDebtAdmin(admin.ModelAdmin):
    """Долги пользователей"""
    list_display = ('pk', 'user', 'name', 'data_1', 'data_2', 'account', 'comment', 'currency', 'sum', 'initial_sum')
    list_filter = ('sum', 'data_1', 'data_2')
    list_display_links = ('user', 'pk', 'name')