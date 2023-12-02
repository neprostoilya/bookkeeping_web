from django.urls import path
from .views import *

urlpatterns = [
    path('', Page.as_view(), name='index'),
    path('manual/', Manual.as_view(), name='manual'),
    # Регистрация и Авторизация
    path('login/', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
    # Счета
    path('accounts/', AccountPage.as_view(), name='accounts'),
    path('accounts/create/', AccountCreate.as_view(), name='create_account'),
    path('accounts/update/<int:pk>/', AccountUpdate.as_view(), name='update_account'),
    path('accounts/transfer/', AccountTransfer.as_view(), name='transfer_account'),
    path('accounts/delete/<int:pk>/', AccountDelete.as_view(), name='delete_account'),
    # Доходы
    path('incomes/', IncomePage.as_view(), name='incomes'),
    path('incomes/create/', IncomeCreate.as_view(), name='create_income'),
    path('incomes/update/<int:pk>/', IncomeUpdate.as_view(), name='update_income'),
    path('incomes/delete/<int:pk>/', IncomeDelete.as_view(), name='delete_income'),
    # Расходы
    path('expenses/', ExpensePage.as_view(), name='expenses'),
    path('expenses/create/', ExpenseCreate.as_view(), name='create_expense'),
    path('expenses/update/<int:pk>/', ExpenseUpdate.as_view(), name='update_expense'),
    path('expenses/delete/<int:pk>/', ExpenseDelete.as_view(), name='delete_expense'),
    # Долги пользователя
    path('owe_debts/', OweDebtPage.as_view(), name='owe_debts'), 
    path('owe_debts/create/', OweDebtCreate.as_view(), name='create_owe_debt'),    
    path('owe_debts/update/<int:pk>/', OweDebtUpdate.as_view(), name='update_owe_debt'),
    path('owe_debts/return/<int:pk>/', OweDebtReturn.as_view(), name='return_owe_debt'), 
    path('owe_debts/delete/<int:pk>/', OweDebtDelete.as_view(), name='delete_owe_debt'),   
    # Долги у пользователя
    path('debts/', DebtPage.as_view(), name='debts'), 
    path('debts/create/', DebtCreate.as_view(), name='create_debt'),    
    path('debts/update/<int:pk>/', DebtUpdate.as_view(), name='update_debt'),
    path('debts/return/<int:pk>/', DebtReturn.as_view(), name='return_debt'), 
    path('debts/delete/<int:pk>/', DebtDelete.as_view(), name='delete_debt'),  
    # Статистика
    path('graphic/accounts/', graph_accounts, name='graphic_accounts'), 
    path('graphic/incomes/', graph_incomes, name='graphic_incomes'), 
    path('graphic/expenses/', graph_expenses, name='graphic_expenses'), 
    ## Категории
    path('categories/accounts/', CategoryAccountPage.as_view(), name='categories_accounts'), 
    path('categories/accounts/create/', CategoryAccountCreate.as_view(), name='create_category_account'), 
    path('categories/accounts/update/<int:pk>/', CategoryAccountUpdate.as_view(), name='update_category_account'), 
    path('categories/accounts/delete/<int:pk>/', CategoryAccountDelete.as_view(), name='delete_category_account'),  
    # 
    path('categories/incomes/', CategoryIncomePage.as_view(), name='categories_incomes'),
    path('categories/incomes/create/', CategoryIncomeCreate.as_view(), name='create_category_income'), 
    path('categories/incomes/update/<int:pk>/', CategoryIncomeUpdate.as_view(), name='update_category_income'), 
    path('categories/incomes/delete/<int:pk>/', CategoryIncomeDelete.as_view(), name='delete_category_income'),  
    # 
    path('categories/expenses/', CategoryExpensePage.as_view(), name='categories_expenses'), 
    path('categories/expenses/create/', CategoryExpenseCreate.as_view(), name='create_category_expense'), 
    path('categories/expenses/update/<int:pk>/', CategoryExpenseUpdate.as_view(), name='update_category_expense'), 
    path('categories/expenses/delete/<int:pk>/', CategoryExpenseDelete.as_view(), name='delete_category_expense'),  
    #
    path('categories/currencys/', CategoryCurrencyPage.as_view(), name='categories_currencys'), 
    path('categories/currencys/create/', CategoryCurrencyCreate.as_view(), name='create_category_currency'), 
    path('categories/currencys/update/<int:pk>/', CategoryCurrencyUpdate.as_view(), name='update_category_currency'), 
    path('categories/currencys/delete/<int:pk>/', CategoryCurrencyDelete.as_view(), name='delete_category_currency'),  
]
