from django.urls import path
from .views import *

urlpatterns = [
    path('', Page.as_view(), name='index'),
    path('login_registration/', login_registration, name='login_registration'),
    path('login_authentication/', login_authentication, name='login_authentication'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('register', register, name='register'),
    path('accounts/', UserAccount.as_view(), name='accounts'),
    # path('create_accounts/', account, name='account'),
    # path('create_account', create_account, name='create_account') # TODO Доделать
]