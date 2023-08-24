from django.contrib import admin

from .models import CategoryExpenses, CategoryIncome, CategoryCurrency, \
                    UserExpenses, UserIncomes, UserAccount, CategoryAccounts

@admin.register(CategoryIncome)
class CategoryIncomesAdmin(admin.ModelAdmin):
    """Категории Доходов"""
    list_display = ('pk', 'user', 'title', 'parent')
    list_display_links = ('title', 'pk')

@admin.register(CategoryExpenses)
class CategoryExpensesAdmin(admin.ModelAdmin):
    """Категории Расходов"""
    list_display = ('pk', 'user', 'title', 'parent')
    list_display_links = ('title', 'pk')

@admin.register(CategoryCurrency)
class CategoryCurrencyAdmin(admin.ModelAdmin):
    """Категории валют"""
    list_display = ('pk', 'user', 'title')
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

@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    """Счета пользователя"""
    list_display = ('pk', 'user', 'account', 'course', 'currency', 'get_course_sum')
    list_filter = ('sum',)
    list_editable = ('account',)
    list_display_links = ('user', 'pk')

@admin.register(CategoryAccounts)
class CategoryAccountsAdmin(admin.ModelAdmin):
    """Категории Счетов"""
    list_display = ('pk', 'user', 'title')
    list_editable = ('title',)

