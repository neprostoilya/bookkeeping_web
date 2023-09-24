from django.urls import path
from .views import *

urlpatterns = [
    path('', Page.as_view(), name='index'),
    # Регистрация и Авторизация
    path('login_registration/', login_registration, name='login_registration'),
    path('login_authentication/', login_authentication, name='login_authentication'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('register', register, name='register'),
    # Счета
    path('accounts/', AccountPage.as_view(), name='accounts'),
    path('accounts/create_account/', AccountCreate.as_view(), name='create_account'),
    path('accounts/update/<int:pk>/', AccountUpdate.as_view(), name='update_account'),
    path('accounts/transfer/', TransferToAccount.as_view(), name='transfer_account'),
    path('accounts/delete/', delete_accounts, name='delete_accounts'),
    # Доходы
    path('incomes/', IncomePage.as_view(), name='incomes'),
    path('incomes/create_income/', IncomeCreate.as_view(), name='create_income'),
    path('incomes/update/<int:pk>/', IncomeUpdate.as_view(), name='update_income'),
    path('incomes/delete/', delete_incomes, name='delete_incomes'),
    # Расходы
    path('expenses/', ExpensePage.as_view(), name='expenses'),
    path('expenses/create_expense/', ExpenseCreate.as_view(), name='create_expense'),
    path('expenses/update/<int:pk>/', ExpenseUpdate.as_view(), name='update_expense'),
    path('expenses/delete/', delete_expenses, name='delete_expenses'),
    # Долги пользователя
    path('owe_debts/', OweDebtPage.as_view(), name='owe_debts'), 
    path('owe_debts/create_owe_debt/', OweDebtCreate.as_view(), name='create_owe_debt'),    
    path('owe_debts/update/<int:pk>/', OweDebtUpdate.as_view(), name='update_owe_debt'),
    path('owe_debts/return_owe_debt/<int:pk>/', OweDebtReturn.as_view(), name='return_owe_debt'), 
    path('owe_debts/delete/', delete_owe_debts, name='delete_owe_debts'),   
    # Долги у пользователя
    path('debts/', DebtPage.as_view(), name='debts'), 
    path('debts/create_debt/', DebtCreate.as_view(), name='create_debt'),    
    path('debts/update/<int:pk>/', DebtUpdate.as_view(), name='update_debt'),
    path('debts/return_debt/<int:pk>/', DebtReturn.as_view(), name='return_debt'), 
    path('debts/delete/', delete_debts, name='delete_debts'),  
    # Статистика
    path('statistics/accounts/', graph_accounts, name='graphic_accounts'), 
    path('statistics/incomes/', graph_incomes, name='graphic_incomes'), 
    path('statistics/expenses/', graph_expenses, name='graphic_expenses'), 
    # Категории
    path('categories/accounts/', CategoriesAccounts.as_view(), name='categories_accounts'), 
    path('categories/incomes/', CategoriesIncomes.as_view(), name='categories_incomes'), 
    path('categories/expenses/', CategoriesExpenses.as_view(), name='categories_expenses'), 
    path('categories/currencys/', CategoriesCurrencys.as_view(), name='categories_currencys'), 
]
