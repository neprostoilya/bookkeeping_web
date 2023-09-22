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
    path('accounts/', UserAccountPage.as_view(), name='accounts'),
    path('accounts/create_accounts/', create_account_page, name='create_accounts'),
    path('accounts/create_account', create_account, name='create_account'),
    path('accounts/transfer_to_account/', transfer_to_account_page, name='transfer_to_account'),
    path('accounts/transfer', transfer, name='transfer_account'),
    path('accounts/update/<int:pk>/', UserAccountUpdate.as_view(), name='update_account'),
    path('accounts/delete/', delete_accounts, name='delete_accounts'),
    # Доходы
    path('incomes/', UserIncomesPage.as_view(), name='incomes'),
    path('incomes/add_incomes/', add_income_page, name='add_incomes'),
    path('incomes/add_income', add_income, name='add_income'),
    path('incomes/update/<int:pk>/', UserIncomesUpdate.as_view(), name='update_income'),
    path('incomes/delete/', delete_expenses, name='delete_expenses'),
    # Расходы
    path('expenses/', UserExpensesPage.as_view(), name='expenses'),
    path('expenses/add_expenses/', add_expenses_page, name='add_expenses'),
    path('expenses/add_expense', add_expense, name='add_expense'),
    path('expenses/update/<int:pk>/', UserExpensesUpdate.as_view(), name='update_expense'),
    path('expenses/delete/', delete_incomes, name='delete_incomes'),
    # Долги пользователя
    path('owe_debts/', UserOweDebtsPage.as_view(), name='owe_debts'), 
    path('owe_debts/update/<int:pk>/', UserOweDebtsUpdate.as_view(), name='update_owe_debts'),
    path('owe_debts/delete/', delete_owe_debts, name='delete_owe_debts'),   
    path('owe_debts/add_owe_debts/', add_owe_debts_page, name='add_owe_debts'),    
    path('owe_debts/add_owe_debt', add_owe_debt, name='add_owe_debt'), 
    path('owe_debts/return_owe_debts/<int:pk>/', UserReturnOweDebts.as_view(), name='return_owe_debts'), 
    # Долги у пользователя
    path('debts/', UserDebtsPage.as_view(), name='debts'), 
    path('debts/update/<int:pk>/', UserDebtsUpdate.as_view(), name='update_debts'),
    path('debts/delete/', delete_debts, name='delete_debts'),   
    path('debts/add_debts/', add_debts_page, name='add_debts'),    
    path('debts/add_debt', add_debt, name='add_debt'), 
    path('debts/return_debts/<int:pk>/', UserReturnDebts.as_view(), name='return_debts'), 
    # Статистика
    path('statistics/accounts/', graph_accounts, name='graphic_accounts'), 
    path('statistics/incomes/', graph_incomes, name='graphic_incomes'), 
    path('statistics/expenses/', graph_expenses, name='graphic_expenses'), 
    # Категории
    path('category/accounts/', UserCategoryAccounts.as_view(), name='category_accounts'), 
    path('category/incomes/', UserCategoryIncomes.as_view(), name='category_incomes'), 
    path('category/expenses/', UserCategoryExpenses.as_view(), name='category_expenses'), 
]
