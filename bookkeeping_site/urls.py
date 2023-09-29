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
    path('activation_code/', activation_code, name='activate'),
    # Счета
    path('accounts/', AccountPage.as_view(), name='accounts'),
    path('accounts/create/', AccountCreate.as_view(), name='create_account'),
    path('accounts/update/<int:pk>/', AccountUpdate.as_view(), name='update_account'),
    path('accounts/transfer/', TransferToAccount.as_view(), name='transfer_account'),
    path('accounts/delete/', delete_accounts, name='delete_accounts'),
    # Доходы
    path('incomes/', IncomePage.as_view(), name='incomes'),
    path('incomes/create/', IncomeCreate.as_view(), name='create_income'),
    path('incomes/update/<int:pk>/', IncomeUpdate.as_view(), name='update_income'),
    path('incomes/delete/', delete_incomes, name='delete_incomes'),
    # Расходы
    path('expenses/', ExpensePage.as_view(), name='expenses'),
    path('expenses/create/', ExpenseCreate.as_view(), name='create_expense'),
    path('expenses/update/<int:pk>/', ExpenseUpdate.as_view(), name='update_expense'),
    path('expenses/delete/', delete_expenses, name='delete_expenses'),
    # Долги пользователя
    path('owe_debts/', OweDebtPage.as_view(), name='owe_debts'), 
    path('owe_debts/create/', OweDebtCreate.as_view(), name='create_owe_debt'),    
    path('owe_debts/update/<int:pk>/', OweDebtUpdate.as_view(), name='update_owe_debt'),
    path('owe_debts/return/<int:pk>/', OweDebtReturn.as_view(), name='return_owe_debt'), 
    path('owe_debts/delete/', delete_owe_debts, name='delete_owe_debts'),   
    # Долги у пользователя
    path('debts/', DebtPage.as_view(), name='debts'), 
    path('debts/create/', DebtCreate.as_view(), name='create_debt'),    
    path('debts/update/<int:pk>/', DebtUpdate.as_view(), name='update_debt'),
    path('debts/return/<int:pk>/', DebtReturn.as_view(), name='return_debt'), 
    path('debts/delete/', delete_debts, name='delete_debts'),  
    # Статистика
    path('graphic/accounts/', graph_accounts, name='graphic_accounts'), 
    path('graphic/incomes/', graph_incomes, name='graphic_incomes'), 
    path('graphic/expenses/', graph_expenses, name='graphic_expenses'), 
    ## Категории
    path('categories/accounts/', CategoryAccountPage.as_view(), name='categories_accounts'), 
    path('categories/accounts/create/', CategoryAccountCreate.as_view(), name='create_category_account'), 
    path('categories/accounts/update/<int:pk>/', CategoryAccountUpdate.as_view(), name='update_category_account'), 
    path('categories/accounts/delete/', delete_categories_accounts, name='delete_categories_accounts'),  
    # 
    path('categories/incomes/', CategoryIncomePage.as_view(), name='categories_incomes'),
    path('categories/incomes/create/', CategoryIncomeCreate.as_view(), name='create_category_income'), 
    path('categories/incomes/update/<int:pk>/', CategoryIncomeUpdate.as_view(), name='update_category_income'), 
    path('categories/incomes/delete/', delete_categories_incomes, name='delete_categories_incomes'),  
    # 
    path('categories/expenses/', CategoryExpensePage.as_view(), name='categories_expenses'), 
    path('categories/expenses/create/', CategoryExpenseCreate.as_view(), name='create_category_expense'), 
    path('categories/expenses/update/<int:pk>/', CategoryExpenseUpdate.as_view(), name='update_category_expense'), 
    path('categories/expenses/delete/', delete_categories_expenses, name='delete_categories_expenses'),  
    #
    path('categories/currencys/', CategoryCurrencyPage.as_view(), name='categories_currencys'), 
    path('categories/currencys/create/', CategoryCurrencyCreate.as_view(), name='create_category_currency'), 
    path('categories/currencys/update/<int:pk>/', CategoryCurrencyUpdate.as_view(), name='update_category_currency'), 
    path('categories/currencys/delete/', delete_categories_currencys, name='delete_categories_currencys'),  
]
