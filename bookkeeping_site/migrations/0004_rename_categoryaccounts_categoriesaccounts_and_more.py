# Generated by Django 4.2.4 on 2023-09-24 20:08

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookkeeping_site', '0003_alter_useraccount_account'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CategoryAccounts',
            new_name='CategoriesAccounts',
        ),
        migrations.RenameModel(
            old_name='CategoryCurrency',
            new_name='CategoriesCurrencys',
        ),
        migrations.RenameModel(
            old_name='CategoryExpenses',
            new_name='CategoriesExpenses',
        ),
        migrations.RenameModel(
            old_name='CategoryIncomes',
            new_name='CategoriesIncomes',
        ),
    ]
