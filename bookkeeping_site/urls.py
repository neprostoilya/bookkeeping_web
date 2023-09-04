from django.urls import path
from .views import *

urlpatterns = [
    path('', Page.as_view(), name='index'),
    path('login_registration/', login_registration, name='login_registration'),
    path('login_authentication/', login_authentication, name='login_authentication'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('register', register, name='register'),
    path('accounts/', UserAccountPage.as_view(), name='accounts'),
    path('accounts/create_accounts/', create_account_page, name='account'),
    path('accounts/create_account', create_account, name='create_account'),
    path('accounts/transfer_to_account/', transfer_to_account_page, name='transfer_to_account'),
    path('accounts/transfer', transfer, name='transfer'),
    path('incomes/', UserIncomesPage.as_view(), name='incomes'),
    path('incomes/add_incomes/', add_income_page, name='add_incomes'),
    path('incomes/add_income', add_income, name='add_income'),
    path('expenses/', UserExpensesPage.as_view(), name='expenses'),
    path('expenses/add_expenses/', add_expenses_page, name='add_expenses'),
    path('expenses/add_expense', add_expense, name='add_expense'),
    path('debts/', UserDebtsPage.as_view(), name='debts'),    
    path('debts/add_debts/', add_debts_page, name='add_debts'),    
    path('debts/add_debt', add_debt, name='add_debt'), 
]