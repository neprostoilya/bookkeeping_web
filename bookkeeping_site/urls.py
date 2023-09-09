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
    path('accounts/update/<int:pk>/', UserAccountUpdate.as_view(), name='update_account'),
    path('accounts/delete/<int:pk>/', UserAccountDelete.as_view(), name='delete_account'),
    path('incomes/', UserIncomesPage.as_view(), name='incomes'),
    path('incomes/add_incomes/', add_income_page, name='add_incomes'),
    path('incomes/add_income', add_income, name='add_income'),
    path('incomes/update/<int:pk>/', UserIncomesUpdate.as_view(), name='update_income'),
    path('incomes/delete/<int:pk>/', UserIncomesDelete.as_view(), name='delete_income'),
    path('expenses/', UserExpensesPage.as_view(), name='expenses'),
    path('expenses/add_expenses/', add_expenses_page, name='add_expenses'),
    path('expenses/add_expense', add_expense, name='add_expense'),
    path('expenses/update/<int:pk>/', UserExpensesUpdate.as_view(), name='update_expense'),
    path('expenses/delete/<int:pk>/', UserExpensesDelete.as_view(), name='delete_expense'),
    path('owe_debts/', UserOweDebtsPage.as_view(), name='owe_debts'),    
    path('owe_debts/add_owe_debts/', add_owe_debts_page, name='add_owe_debts'),    
    path('owe_debts/add_owe_debt', add_owe_debt, name='add_owe_debt'), 
    path('owe_debts/update/<int:pk>/', UserOweDebtsUpdate.as_view(), name='update_owe_debt'),
    path('owe_debts/delete/<int:pk>/', UserOweDebtsDelete.as_view(), name='delete_owe_debt'),
    path('debts/', UserDebtsPage.as_view(), name='debts'), 
    path('debts/update/<int:pk>/', UserDebtsUpdate.as_view(), name='update_debt'),
    path('debts/delete/<int:pk>/', UserDebtsDelete.as_view(), name='delete_debt'),   
    path('debts/add_debts/', add_debts_page, name='add_debts'),    
    path('debts/add_debt', add_debt, name='add_debt'), 
]
