# Generated by Django 4.2.4 on 2023-08-19 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookkeeping_site', '0006_alter_userexpenses_parent_userincomes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userexpenses',
            name='account',
        ),
        migrations.RemoveField(
            model_name='userexpenses',
            name='category',
        ),
        migrations.RemoveField(
            model_name='userexpenses',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='userexpenses',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userincomes',
            name='account',
        ),
        migrations.RemoveField(
            model_name='userincomes',
            name='category',
        ),
        migrations.RemoveField(
            model_name='userincomes',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='userincomes',
            name='user',
        ),
        migrations.DeleteModel(
            name='CategoryAccounts',
        ),
        migrations.DeleteModel(
            name='CategoryCurrency',
        ),
        migrations.DeleteModel(
            name='UserExpenses',
        ),
        migrations.DeleteModel(
            name='UserIncomes',
        ),
    ]
