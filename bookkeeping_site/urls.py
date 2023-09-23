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
    path('accounts/create_account/', UserAccountCreate.as_view(), name='create_account'),
    path('accounts/update/<int:pk>/', UserAccountUpdate.as_view(), name='update_account'),
    path('accounts/transfer_to_account/', transfer_to_account_page, name='transfer_to_account'),
    path('accounts/transfer', transfer, name='transfer_account'),
    path('accounts/delete/', delete_accounts, name='delete_accounts'),
    # Доходы
    path('incomes/', UserIncomePage.as_view(), name='incomes'),
    path('incomes/create_income/', UserIncomeCreate.as_view(), name='create_income'),
    path('incomes/update/<int:pk>/', UserIncomeUpdate.as_view(), name='update_income'),
    path('incomes/delete/', delete_incomes, name='delete_incomes'),
    # Расходы
    path('expenses/', UserExpensePage.as_view(), name='expenses'),
    path('expenses/create_expense/', UserExpenseCreate.as_view(), name='create_expense'),
    path('expenses/update/<int:pk>/', UserExpenseUpdate.as_view(), name='update_expense'),
    path('expenses/delete/', delete_expenses, name='delete_expenses'),
    # Долги пользователя
    path('owe_debts/', UserOweDebtPage.as_view(), name='owe_debts'), 
    path('owe_debts/create_owe_debt/', UserOweDebtCreate.as_view(), name='create_owe_debt'),    
    path('owe_debts/update/<int:pk>/', UserOweDebtUpdate.as_view(), name='update_owe_debt'),
    path('owe_debts/return_owe_debt/<int:pk>/', UserOweDebtReturn.as_view(), name='return_owe_debt'), 
    path('owe_debts/delete/', delete_owe_debts, name='delete_owe_debts'),   
    # Долги у пользователя
    path('debts/', UserOweDebtPage.as_view(), name='debts'), 
    path('debts/create_debt/', UserDebtCreate.as_view(), name='create_debt'),    
    path('debts/update/<int:pk>/', UserDebtUpdate.as_view(), name='update_debt'),
    path('debts/return_debt/<int:pk>/', UserDebtReturn.as_view(), name='return_debt'), 
    path('debts/delete/', delete_debts, name='delete_debts'),  
    # Статистика
    path('statistics/accounts/', graph_accounts, name='graphic_accounts'), 
    path('statistics/incomes/', graph_incomes, name='graphic_incomes'), 
    path('statistics/expenses/', graph_expenses, name='graphic_expenses'), 
    # Категории
    path('category/accounts/', UserCategoryAccounts.as_view(), name='category_accounts'), 
    path('category/incomes/', UserCategoryIncomes.as_view(), name='category_incomes'), 
    path('category/expenses/', UserCategoryExpenses.as_view(), name='category_expenses'), 
]
